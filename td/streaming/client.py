from collections import defaultdict
import inspect
import urllib
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
from websockets import client as ws_client
from websockets import exceptions as ws_exceptions
import simplejson as json

from td.enums.enums import ServiceState, StreamApiResponse
from td.logger import TdLogger
from td.rest.user_info import UserInfo
from td.session import TdAmeritradeSession
from td.streaming.services import StreamingServices


class ShutdownException(Exception):
    """Exception raised when a shutdown event is detected."""

    pass


class StreamingApiClient:
    """
    Implements a Websocket object that connects to the TD
    Streaming API, submits requests, handles messages, and
    streams data back to the user.
    """

    def __init__(
        self,
        session: TdAmeritradeSession,
        on_message_received=None,
        on_stream_restarted=None,
        log_received_messages=False,
        log_sent_messages=True,
    ) -> None:
        """
        Initalizes the Streaming Client which handles websocket based requests for the
        TD Streaming API in an event loop.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
        """
        self._services = None

        self._websocket_lock = asyncio.Lock()
        self._req_num_lock = asyncio.Lock()
        self._data_requests_lock = asyncio.Lock()
        self._subscribed_services_lock = asyncio.Lock()
        self._handlers_lock = asyncio.Lock()
        self._restart_lock = asyncio.Lock()

        self.user_principal_data = UserInfo(session=session).get_user_principals()
        socket_url = self.user_principal_data["streamerInfo"]["streamerSocketUrl"]
        self.websocket_url = f"wss://{socket_url}/ws"

        self._on_message_received = on_message_received
        self._on_stream_restarted = on_stream_restarted
        self.is_stream_restarted = False

        self._handlers = defaultdict(list)
        self.subscribed_services = {}
        self.data_requests = {"requests": []}

        self.log = TdLogger(__name__).logger
        self._log_debug_enabled = self.log.isEnabledFor(logging.DEBUG)
        self._log_received_messages = log_received_messages
        self._log_sent_messages = log_sent_messages
        self.request_number = -1

        self._connection: ws_client.WebSocketClientProtocol | None = None

        self.logged_in_event = asyncio.Event()
        self.shutdown_event = asyncio.Event()
        self.loop = None
        self.background_tasks = set()
        self.background_thread = None

        # Grab the token timestamp.
        token_timestamp = self.user_principal_data["streamerInfo"]["tokenTimestamp"]
        token_timestamp = datetime.strptime(token_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        token_timestamp = int(token_timestamp.timestamp()) * 1000

        # Define our Credentials Dictionary used for authentication.
        self.credentials = {
            "userid": self.user_principal_data["accounts"][0]["accountId"],
            "token": self.user_principal_data["streamerInfo"]["token"],
            "company": self.user_principal_data["accounts"][0]["company"],
            "segment": self.user_principal_data["accounts"][0]["segment"],
            "cddomain": self.user_principal_data["accounts"][0]["accountCdDomainId"],
            "usergroup": self.user_principal_data["streamerInfo"]["userGroup"],
            "accesslevel": self.user_principal_data["streamerInfo"]["accessLevel"],
            "authorized": "Y",
            "timestamp": token_timestamp,
            "appid": self.user_principal_data["streamerInfo"]["appId"],
            "acl": self.user_principal_data["streamerInfo"]["acl"],
        }

    @property
    def is_stream_restarted(self) -> bool:
        """Returns a boolean value indicating if the stream was restarted."""
        return self._is_stream_restarted

    @is_stream_restarted.setter
    def is_stream_restarted(self, value: bool):
        """Set whether the stream was restarted or not."""
        self._is_stream_restarted = value

    @property
    def services(self) -> StreamingServices:
        """
        Returns the streaming services that can be added
        either before or while the stream runs.

        Returns
        ----
        StreamingServices
            The `StreamingServices` offered by the API.

        Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
        """
        if self._services:
            return self._services
        self._services = StreamingServices(streaming_api_client=self)
        return self._services

    @services.setter
    def services(self, value):
        self._services = value

    async def _req_num(self) -> int:
        """Increments and returns the request number"""
        async with self._req_num_lock:
            self.request_number += 1
        return self.request_number

    def _run_threadsafe_wrapper(self, func_to_run, *args):
        """Runs with background thread event loop or main thread loop."""
        if self.background_thread and self.background_thread != threading.main_thread():
            return asyncio.run_coroutine_threadsafe(
                func_to_run(*args), self.loop
            ).result()
        with ThreadPoolExecutor(1) as executor:
            future = executor.submit(
                asyncio.run_coroutine_threadsafe, func_to_run(*args), self.loop
            )
            return future.result()

    async def _add_data_request(self, request: dict) -> int:
        """Adds a data request to be sent"""
        await self.logged_in_event.wait()
        async with self._data_requests_lock:
            request["requestid"] = await self._req_num()
            self.data_requests["requests"].append(request)

        service = request["service"]
        if not self.subscribed_services.get(service, None):
            await self._add_subscribed_service(service)
        return request["requestid"]

    def add_data_request(self, request: dict) -> int:
        """Adds a data request to be sent"""
        return self._run_threadsafe_wrapper(self._add_data_request, request)

    # ADMIN - LOGIN
    async def _build_login_request(self) -> dict:
        """
        Builds login request.

        Returns
        ----
        int
            Request number
        """
        request = self.services.service_helper(service="ADMIN", command="LOGIN")
        del request["parameters"]["keys"]
        del request["parameters"]["fields"]

        request["parameters"]["credential"] = urllib.parse.urlencode(self.credentials)
        request["parameters"]["token"] = self.user_principal_data["streamerInfo"][
            "token"
        ]
        request["parameters"]["version"] = "1.0"

        request["requestid"] = await self._req_num()

        return {"requests": [request]}

    async def _add_subscribed_service(
        self, service: str, service_state: ServiceState = ServiceState.ACKED
    ) -> None:
        """Adds a subscribed service."""

        async with self._subscribed_services_lock:
            self.subscribed_services[service] = service_state

            if service_state == ServiceState.ACKED:
                self.log.debug(f"Attempting to Add Service - {service}")
            elif service_state == ServiceState.SUBSCRIBED:
                self.log.debug(f"Successful Add Service - {service}")

    async def _remove_subscribed_service(
        self, service: str, failed_add=False, content=None
    ) -> None:
        """Removes a subscribed service."""

        async with self._subscribed_services_lock:
            if self.subscribed_services.get(service, None):
                del self.subscribed_services[service]
                if not failed_add:
                    self.log.debug(f"Removed Service -  {service}")
                else:
                    self.log.error(f"Failed Add Service - {service}, {content}")

    async def _add_handler(self, response_type: str, service: str, func_) -> None:
        """Adds a handler for a received message"""

        async with self._handlers_lock:
            self._handlers[(response_type, service)].append(func_)

    def add_handler(self, response_type: str, service: str, func_) -> None:
        """Adds a handler for a received message"""

        return self._run_threadsafe_wrapper(
            self._add_handler, response_type, service, func_
        )

    async def _remove_handler(self, response_type: str, service: str, func_):
        """Removes a handler for a received message"""
        async with self._handlers_lock:
            if self._handlers.get((response_type, service), None):
                try:
                    self._handlers[(response_type, service)].remove(func_)
                except ValueError:
                    self.log.error(
                        f"Not in handlers / already removed?\n {response_type} - {service} - {func_}"
                    )

    def remove_handler(self, response_type: str, service: str, func_):
        """Removes a handler for a received message"""

        return self._run_threadsafe_wrapper(
            self._remove_handler, response_type, service, func_
        )

    async def _has_handler(self, response_type: str, service: str, func_):
        """Removes a handler for a received message"""
        async with self._handlers_lock:
            if self._handlers.get((response_type, service), None):
                try:
                    handler = self._handlers[(response_type, service)]
                    if handler == func_:
                        return True
                except ValueError:
                    return False
            return False

    def has_handler(self, response_type: str, service: str, func_):
        """Checks if a specific handler exists"""

        return self._run_threadsafe_wrapper(
            self._has_handler, response_type, service, func_
        )

    async def _send_data_requests(self):
        """Sends the data requests added, forever."""

        await self.logged_in_event.wait()

        # Send the data requests, and start getting messages.
        while not self.shutdown_event.is_set():
            await asyncio.sleep(0.1)
            async with self._data_requests_lock:
                if not self.data_requests["requests"]:
                    continue

                data_requests = json.dumps(self.data_requests)
                self.data_requests = {"requests": []}
            try:
                data_request_task = self.loop.create_task(
                    self._send_message(data_requests)
                )
                self.background_tasks.add(data_request_task)
                data_request_task.add_done_callback(self.background_tasks.discard)
            except ws_exceptions.ConnectionClosed:
                try:
                    self.log.debug(
                        "_send_data_requests - ws_exceptions.ConnectionClosed exception - attempting to restart"
                    )
                    async with self._restart_lock:
                        await self._restart_stream()
                except Exception as restart_stream_error:
                    self.log.error(
                        f"Error while restarting the stream: {restart_stream_error}"
                    )
                    raise  # This will re-raise the exception to the calling function
                try:
                    data_request_task = self.loop.create_task(
                        self._send_message(data_requests)
                    )
                    self.background_tasks.add(data_request_task)
                    data_request_task.add_done_callback(self.background_tasks.discard)
                except Exception as e:
                    self.log.error("Error after restarting in data_requests... %s", e)

    async def _connect(self, restart=False) -> None:
        """Connects the Client to the TD Websocket or attempts to reconnect."""
        async with self._websocket_lock:
            try:
                self._connection = await ws_client.connect(
                    self.websocket_url, max_size=2048000
                )
            except ws_exceptions.WebSocketException as e:
                raise e
            except Exception as e:
                raise e

        login_request = await self._build_login_request()
        self.subscribed_services = {}
        await self._add_subscribed_service("ADMIN")
        await self._send_message(json.dumps(login_request))

        while not self.shutdown_event.is_set():
            # Grab the Response.
            response = await self._receive_message(return_value=True)
            responses = response.get("response", None)

            if responses:
                for r in responses:
                    command = r.get("command", None)
                    service = r.get("service", None)
                    if command and service:
                        if command == "LOGIN" and service == "ADMIN":
                            if r["content"]["code"] == 3:
                                login_error_msg = (
                                    f"LOGIN ERROR: {responses[0]['content']['msg']}"
                                )
                                self.log.error(login_error_msg)
                                raise ValueError(login_error_msg)
                            elif r["content"]["code"] == 0:
                                await self._add_subscribed_service(
                                    "ADMIN", ServiceState.SUBSCRIBED
                                )
                                if not restart:
                                    self.log.info(
                                        "Message: User Login successful, streaming will being shortly."
                                    )
                                else:
                                    self.log.info(
                                        "Connection restarted, User Login successful."
                                    )
                                self.logged_in_event.set()
                                return

    async def _send_message(self, message: str) -> None:
        """Sends a message to webSocket server

        Parameters
        ----
        message: str
            The JSON string with the data streaming
            service subscription.
        """
        if self._log_debug_enabled and self._log_sent_messages:
            modified_data = json.loads(message)
            # Remove the credential and token fields from the copy
            for req in modified_data["requests"]:
                params = req["parameters"]
                if "credential" in params:
                    params["credential"] = "<redacted>"
                if "token" in params:
                    params["token"] = "<redacted>"

            # Log the modified message
            log_safe_message = json.dumps(modified_data)
            self.log.debug(f"Sending message:\n{log_safe_message}")

        async with self._websocket_lock:
            await self._connection.send(message)

    async def _receive_message(self, return_value: bool = False) -> dict:
        """Receives and processes the messages as needed.

        Parameters
        ----
        return_value: bool (optional, Default=False)
            Specifies whether the messages should be returned
            back to the calling function or not.

        Returns
        ----
        dict:
            The streaming message.
        """
        response_types = StreamApiResponse.all_values()

        while not self.shutdown_event.is_set():
            try:
                async with self._websocket_lock:
                    message = await self._connection.recv()
                msg = await self._parse_json_message(message=message)

                if self._log_debug_enabled and self._log_received_messages:
                    self.log.debug(msg)

                if "notify" in msg:
                    for r in msg["notify"]:
                        service = r.get("service", None)
                        content = r.get("content", None)
                        if service and content:
                            content_msg = content.get("msg", None)
                            if content_msg:
                                if service == "ADMIN":
                                    # capture Stop streaming due to empty subscription
                                    #  and other potential admin messages
                                    self.log.info(content["msg"])
                                    if (
                                        content_msg
                                        == "Stop streaming due to empty subscription"
                                    ):
                                        # If server says we aren't subscribed to anything then set it as such
                                        self.subscribed_services = {}
                                        self.logged_in_event.clear()

                if "response" in msg or "snapshot" in msg:
                    received_type = None
                    if "snapshot" in msg:
                        received_type = "snapshot"
                    else:
                        received_type = "response"
                    for r in msg[received_type]:
                        service = r.get("service", None)
                        command = r.get("command", None)

                        if service and command:
                            if command == "SUBS":
                                content = r.get("content", None)
                                if content:
                                    code = content.get("code", None)
                                    if code == 0:
                                        await self._add_subscribed_service(
                                            service,
                                            service_state=ServiceState.SUBSCRIBED,
                                        )
                                    else:
                                        await self._remove_subscribed_service(
                                            service, failed_add=True, content=content
                                        )
                            elif command == "GET":
                                await self._add_subscribed_service(
                                    service, service_state=ServiceState.SUBSCRIBED
                                )
                            elif command == "UNSUBS":
                                await self._remove_subscribed_service(service)

                if self._on_message_received:
                    result = self._on_message_received(msg)
                    if inspect.isawaitable(result):
                        asyncio.ensure_future(result)

                if any(key in msg for key in response_types):
                    for type_ in response_types:
                        if type_ in msg:
                            for d in msg[type_]:
                                service = d.get("service", None)
                                if service:
                                    if (type_, service) in self._handlers:
                                        for handler in self._handlers[(type_, service)]:
                                            result = handler(d)
                                            if inspect.isawaitable(result):
                                                asyncio.ensure_future(result)

                if return_value:
                    return msg
            except ws_exceptions.ConnectionClosed:
                try:
                    async with self._restart_lock:
                        self.log.debug(
                            "_receive_message - attempting to restart stream"
                        )
                        await self._restart_stream()
                except Exception as restart_stream_error:
                    self.log.error(
                        f"Error while restarting the stream: {restart_stream_error}"
                    )
                    raise
                self.log.warning("Stream restarted while receiving messages")
                continue
            except Exception as e:
                self.log.error(e)
                return

    async def _resume_connection(self):
        self.log.debug(
            "Waiting for new request / subscription before restarting stream"
        )
        while len(self.subscribed_services) == 0:
            await asyncio.sleep(0.5)
        self.log.debug(
            f"Received new request / subscription. Subscribed services is {self.subscribed_services}"
        )

    async def await_awaitable(self, awaitable):
        awaitable_task = self.loop.create_task(awaitable)
        awaitable_task.add_done_callback(self.background_tasks.discard)

    async def _parse_json_message(self, message: str) -> dict:
        """Parses incoming messages from the stream

        Parameters
        ----
        message: str
            A JSON string needing to be parsed.

        Returns
        ----
        dict:
            The parsed message content.
        """

        # Replace bad characters
        #  inserts a question mark instead of the unencodable character
        message = message.encode("utf-8", "replace").decode("utf-8")

        # Replace common replacements
        message = (
            message.replace("\\\\", "\\").replace("\u0000", "").replace("\x00", "")
        )

        # Load JSON
        try:
            return json.loads(message)
        except json.JSONDecodeError as e:
            self.log.error(e)
            message = f"Failed to parse message:\n{message}\n trying non-strict load"
            self.log.error(message)

            return json.loads(message, strict=False)

    async def _restart_stream(self, initial_delay=1, max_delay=300, backoff_factor=3):
        """Attempt to restart the stream up to max_delay."""

        if self._connection.open:
            return

        await self._resume_connection()

        delay = initial_delay
        attempt = 0
        while delay <= max_delay:
            try:
                self.log.error(
                    f"Restart Stream - Connection closed, attempting to restart stream... (attempt {attempt}, delay {delay}s)"
                )
                await self._connect(restart=True)
                self.is_stream_restarted = True
                if (
                    self._on_stream_restarted
                ):  # Call the callback function if it's defined
                    result = self._on_stream_restarted()
                    if inspect.isawaitable(result):
                        asyncio.ensure_future(result)
                return
            except ws_exceptions.ConnectionClosed:
                pass
            except ws_exceptions.WebSocketException as e:
                self.log.error(
                    f"Restart Stream - Other WebSocketException occurred: {e}"
                )
            except Exception as e:
                self.log.error(f"Restart Stream - Unexpected error occurred: {e}")

            attempt += 1
            delay *= backoff_factor
            delay = min(delay, max_delay)
            await asyncio.sleep(delay)

        raise Exception(
            "Unable to restart connection: Exceeded maximum number of attempts"
        )

    async def _await_shutdown(self):
        """
        Waits for the shutdown event, then raises a ShutdownException.

        Currently, only relevant for internal event loop.
        """
        await self.shutdown_event.wait()
        raise ShutdownException

    async def _open_stream(
        self, outside_managed_loop: asyncio.BaseEventLoop | None = None
    ):
        """
        Opens the stream and handles tasks related to sending data requests,
        receiving messages, and managing shutdown events.

        Args:
            outside_managed_loop (asyncio.BaseEventLoop, optional): An externally managed
            asyncio event loop, if any. If None, the function creates a new event loop.
        """
        try:
            await self._connect()

            send_data_task = self.loop.create_task(self._send_data_requests())
            self.background_tasks.add(send_data_task)

            receive_message_task = self.loop.create_task(self._receive_message())
            self.background_tasks.add(receive_message_task)

            shutdown_task = self.loop.create_task(self._await_shutdown())
            self.background_tasks.add(shutdown_task)

            if not outside_managed_loop:
                await self.shutdown_event.wait()
        except ShutdownException:
            self.background_tasks.discard(send_data_task)
            self.background_tasks.discard(receive_message_task)
            self.background_tasks.discard(shutdown_task)
        finally:
            # shut it down / cleanup
            pass

    def open_stream(self, outside_managed_loop: asyncio.BaseEventLoop | None = None):
        """
        Opens the stream and handles tasks related to sending data requests,
        receiving messages, and managing shutdown events.

        Args:
            outside_managed_loop (asyncio.BaseEventLoop, optional): An externally managed
            asyncio event loop, if any. If None, the function creates a new event loop.
        """

        if outside_managed_loop:
            self.loop = outside_managed_loop
            asyncio.run_coroutine_threadsafe(
                self._open_stream(outside_managed_loop), outside_managed_loop
            )
        else:
            self.loop = asyncio.new_event_loop()
            self.background_thread = threading.Thread(
                target=self.loop.run_until_complete,
                args=[self._open_stream(outside_managed_loop)],
                daemon=True,
            )
            self.background_thread.start()


# TODO: implement close_stream/shutdown/logout
#     async def _shutdown(self):
#         """Closes the connection to the streaming service."""

#         # Close the connection.
#         if self._connection:
#             await self._connection.close()

#         # Shutdown all asynchronous generators.
#         await self.loop.shutdown_asyncgens()

#         # Stop the loop.
#         if self.loop.is_running():
#             self.loop.call_soon_threadsafe(self.loop.stop())
#             await asyncio.sleep(3)
#             self.loop.close()

#         # Check whether the WebSocket connection and event loop are closed.
#         websocket_closed = not self._connection or self._connection.closed

#         # Define the message.
#         closing_message = f"CLOSING PROCESS INITIATED\nWebSocket Closed: {websocket_closed}\nEvent Loop Stop Requested"

#         # Log the message.
#         self.log.info(closing_message)

#         if self.background_thread:
#             if self.background_thread.ident != threading.get_ident():
#                 self.background_thread.join()

#     def close_stream(self):
#         """Closes the connection to the streaming service."""

#         try:
#             asyncio.run_coroutine_threadsafe(self._close_stream(), self.loop)
#         except Exception as e:
#             self.log.error("Error occurred while closing the stream: %s", e)
