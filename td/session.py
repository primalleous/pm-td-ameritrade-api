import json
import requests
import logging
import copy
from requests.exceptions import RequestException
from td.logger import TdLogger


def build_error_dict(response):
    response.request.headers["Authorization"] = "Bearer XXXXXXX"
    response_data = "" if len(response.content) == 0 else response.json()
    return {
        "error_code": response.status_code,
        "response_url": response.url,
        "response_body": response_data,
        "response_request": dict(response.request.headers),
        "response_method": response.request.method,
    }


class TdAmeritradeSession:
    """Serves as the Session for TD Ameritrade API."""

    def __init__(
        self,
        td_client: "TdAmeritradeClient",
        log_received_messages=False,
        log_sent_messages=True,
    ) -> None:
        """Initializes the `TdAmeritradeSession` client.

        Overview
        ----
        The `TdAmeritradeSession` object handles all the requests made
        for the different endpoints on the TD Ameritrade API.

        Parameters
        ----
        client : object
            The `TdAmeritradeClient` Python Client.

        Usage:
        ----
            >>> td_session = TdAmeritradeSession()
        """

        self.client = td_client
        self.resource_url = "https://api.tdameritrade.com/"
        self.version = "v1/"

        self.log = TdLogger(__name__).logger
        self._log_debug_enabled = self.log.isEnabledFor(logging.DEBUG)
        self._log_received_messages = log_received_messages
        self._log_sent_messages = log_sent_messages
        self.request_number = -1

    def _req_num(self) -> int:
        self.request_number += 1
        return self.request_number

    def build_headers(self) -> dict:
        """Used to build the headers needed to make the request.

        Parameters
        ----
        mode: str, optional
            The content mode the headers is being built for, by default `json`.

        Returns
        ----
        Dict:
            A dictionary containing all the components.
        """

        headers = {
            "Authorization": f"Bearer {self.client.td_credentials.access_token}",
            "Content-Type": "application/json",
        }

        return headers

    def build_url(self, endpoint: str) -> str:
        """Build the URL used the make string.

        Parameters
        ----
        endpoint : str
            The endpoint used to make the full URL.

        Returns
        ----
        str:
            The full URL with the endpoint needed.
        """

        url = self.resource_url + self.version + endpoint

        return url

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        json_payload: dict = None,
        timeout: int = None,
    ) -> dict:
        """Handles all the requests in the library.

        Overview
        ---
        A central function used to handle all the requests made in the library,
        this function handles building the URL, defining Content-Type, passing
        through payloads, and handling any errors that may arise during the
        request.

        Parameters
        ----

        method : str
            The Request method, can be one of the following:
            ['get','post','put','delete','patch']

        endpoint : str
            The API URL endpoint, example is 'quotes'

        params : dict (optional, Default=None)
            The URL params for the request.

        data : dict (optional, Default=None)
            A data payload for a request.

        json_payload : dict (optional, Default=None)
            A JSON data payload for a request.

        timeout: int (optional, Default=None)
            The number of seconds to wait for a response before timing out.

        Returns
        ----
        Dict:
            A Dictionary object containing the
            JSON values.
        """

        self.client.td_credentials.validate_token()

        url = self.build_url(endpoint=endpoint)

        headers = self.build_headers()

        request_number = self._req_num()

        self.log.info(
            f"REST request number: {request_number}, Method: {method.upper()}, URL: {url}"
        )

        session = requests.Session()
        session.verify = True

        req = requests.Request(
            method=method.upper(),
            headers=headers,
            url=url,
            params=params,
            data=data,
            json=json_payload,
        )

        if self._log_debug_enabled and self._log_sent_messages:
            temp_req = copy.copy(req)
            temp_req.headers = {"Authorization": "<redacted>"}
            self.log.debug(
                f"REST request number: {request_number}, Request details: {temp_req.__dict__}"
            )

        try:
            response: requests.Response = session.send(
                request=req.prepare(), timeout=timeout
            )
            self.log.info(f"REST request number: {request_number}, Response received.")
        except RequestException as e:
            self.log.error(
                f"REST request number: {request_number}, Request failed with error: {str(e)}"
            )
            raise e

        session.close()

        if response.ok and len(response.content):
            if self._log_debug_enabled and self._log_received_messages:
                self.log.debug(
                    f"REST request number: {request_number}, Response details: {response.json()}"
                )
            return response.json()
        elif len(response.content) == 0 and response.ok:
            return {
                "message": "response ok - no content",
                "status_code": response.status_code,
                "headers": response.headers,
            }

        error_msg = f"REST request number: {request_number}, Request failed status code: {response.status_code}"
        if response.content:
            error_msg += f", Error message: {response.content}"

        try:
            self.log.error(error_msg)
            self.log.error(msg=json.dumps(obj=build_error_dict(response), indent=4))
        except Exception as e:
            self.log.critical(f"Failed to log error: {error_msg}. Exception: {str(e)}")

        raise requests.HTTPError(error_msg)
