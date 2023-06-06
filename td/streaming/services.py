from datetime import date, datetime
from enum import Enum
from typing import List

from td.enums.enums import (
    ActivesDurations,
    ActivesServices,
    ActivesVenues,
    ChartFuturesFrequencies,
    ChartFuturesPeriods,
    ChartHistoryServices,
    ChartServices,
    LevelOneServices,
    LevelTwoQuotes,
    LevelTwoServices,
    NewsServices,
    QOSLevel,
    TimesaleServices,
)
from td.models.streaming import (
    ChartEquityData,
    ChartFuturesOrOptionsData,
    LevelOneEquityData,
    LevelOneForexData,
    LevelOneFuturesData,
    LevelOneFuturesOptionsData,
    LevelOneOptionData,
    NewsHeadlineData,
    TimesaleData,
)
from td.utils.helpers import convert_to_unix_time_ms


class StreamingServices:
    """
    Represents the different streaming services from which data can be pulled.
    """

    def __init__(self, streaming_api_client) -> None:
        """
        Initializes the `StreamingServices` object with a `StreamingApiClient`.

        Parameters
        ----------
        streaming_api_client : StreamingApiClient
            The streaming API client used to send requests.
        """

        from td.streaming.client import StreamingApiClient

        self.stream_client: StreamingApiClient = streaming_api_client

    def new_request_template(self) -> dict:
        """
        Serves as a template to build new service requests.

        Returns
        -------
        dict
            A service request template.
        """

        return {
            "service": None,
            "requestid": None,
            "command": None,
            "account": self.stream_client.user_principal_data["accounts"][0][
                "accountId"
            ],
            "source": self.stream_client.user_principal_data["streamerInfo"]["appId"],
            "parameters": {"keys": None, "fields": None},
        }

    def service_helper(
        self,
        service: str | Enum,
        symbols: List[str] | None = None,
        fields: List[str] | List[int] | None = None,
        command: str | Enum = "SUBS",
    ) -> dict:
        """
        A helper function that simplifies the creation and handling of service requests.

        Parameters
        ----------
        service : str | Enum
            The service to which you wish to subscribe.

        symbols : List[str], (optional, default=None)
            The symbols pertaining to the service request.

        fields : List[str] | List[int], (optional, default=None)
            The data fields to be returned from the endpoint. Can be str or int.

        command : str | Enum, (optional, default="SUBS)
            The command type for the service request.

        Returns
        -------
        dict
            Returns the formatted service request as a dictionary
        """

        request = self.new_request_template()

        if isinstance(service, Enum):
            service = service.value

        if symbols:
            if isinstance(symbols, list):
                request["parameters"]["keys"] = ",".join(symbols)

        if fields:
            if isinstance(fields, list):
                new_fields = []
                for field in fields:
                    if isinstance(field, int):
                        field = str(field)
                    elif isinstance(field, Enum):
                        field = field.value
                    new_fields.append(field)
                fields = new_fields
                request["parameters"]["fields"] = ",".join(fields)

        if isinstance(command, Enum):
            command = command.value

        request["service"] = service
        request["command"] = command

        return request

    # ADMIN
    # ADMIN - LOGOUT
    async def logout(self) -> int:
        """
        Adds logout request to be handled by stream client.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(service="ADMIN", command="LOGOUT")
        del request["parameters"]["keys"]
        del request["parameters"]["fields"]

        return self.stream_client.add_data_request(request)

    # ADMIN - QOS
    def quality_of_service(self, qos_level: str | QOSLevel) -> int:
        """
        Allows the user to set the speed at which they recieve
        messages from the TD Server.

        Parameters
        ----
        qos_level: str | Enum
            The Quality of Service level that you wish to set.
            Ranges from 0 to 5 where 0 is the fastest and 5 is
            the slowest.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.quality_of_service(
                qos_level=QOSLevel.EXPRESS
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(service="ADMIN", command="QOS")

        if isinstance(qos_level, Enum):
            qos_level = qos_level.value

        request["parameters"]["qoslevel"] = qos_level
        return self.stream_client.add_data_request(request)

    # ACCT_ACTIVITY
    def account_activity(self) -> int:
        """
        Represents the ACCOUNT_ACTIVITY endpoint of the TD
        Streaming API. This service is used to request streaming
        updates for one or more accounts associated with
        the logged in User ID. Common usage would involve issuing
        the OrderStatus API request to get all transactions for an
        account, and subscribing to ACCT_ACTIVITY to get any updates.

        Returns
        ----
        int
            Request number
        """

        sub_keys = self.stream_client.user_principal_data["streamerSubscriptionKeys"]
        keys = [sub_keys["keys"][0]["key"]]

        request = self.service_helper(
            "ACCT_ACTIVITY", symbols=keys, fields=["0", "1", "2", "3"]
        )
        return self.stream_client.add_data_request(request)

    # ACTIVES
    # TODO: Quality of life improvements (split up into nyse_actives, options_actives...)
    def actives(
        self,
        service: str | ActivesServices,
        venue: str | ActivesVenues,
        duration: str | ActivesDurations,
    ) -> int:
        """
        Stream most actively traded stocks for a specific exchange.

        Parameters
        ---
        service: str | ActivesServices
            One of the different actives services. For a full
            list please refer to the `enums` file - ActivesServices.

        venue: str | ActivesVenues
            One of the exchanges. For a full
            list please refer to the `enums` file - ActivesVenues.

        duration: str | ActivesDurations
            Specifies the look back period for collecting most
            actively traded instrument. For a full list please
            refer to the `enums` file - ActivesDurations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.actives(
                service=ActivesServices.ActivesNasdaq,
                venue=ActivesVenues.NasdaqExchange,
                duration=ActivesDurations.All
            )

        Returns
        ----
        int
            Request number
        """

        if isinstance(venue, Enum):
            venue = venue.value

        if isinstance(duration, Enum):
            duration = duration.value

        fields = ["1"]  # 1 = Actives Data

        request = self.service_helper(service=service, fields=fields)
        request["parameters"]["keys"] = venue + "-" + duration
        return self.stream_client.add_data_request(request)

    # CHART
    def chart(
        self,
        service: str | ChartServices,
        symbols: List[str],
        fields: List[str] | List[int],
    ) -> int:
        """
        Subscribes to the Chart Service.

        Overview
        ----
        Represents the CHART_EQUITY, CHART_FUTURES, and CHART_OPTIONS endpoint that can
        be used to stream info needed to recreate charts.

        Parameters
        ---
        service: str | ChartServices
            The type of Chart Service you wish to recieve.

        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields :
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.chart(
                service=ChartServices.ChartEquity,
                symbols=["MSFT", "GOOG", "AAPL"],
                fields=ChartEquity.All
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(service, symbols, fields)
        if service in self.stream_client.subscribed_services:
            request["command"] = "ADD"
        return self.stream_client.add_data_request(request)

    # CHART - CHART_EQUITY
    def equity_chart_minute_ohlcv(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = ChartEquityData.get_field_aliases(),
    ) -> int:
        """
        Provides access to equity chart data.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for chart data.

        fields :
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.equity_chart_minute_ohlcv(
                symbols=["SPY"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.chart(
            service=ChartServices.CHART_EQUITY.value, symbols=symbols, fields=fields
        )

    def equity_unsub_chart(self):
        """
        Unsubscribe from equity chart service.

        Returns
        ----
        int
            Request number
        """
        if (
            ChartServices.CHART_EQUITY.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(ChartServices.CHART_EQUITY.value)

    # CHART - CHART_FUTURES
    def futures_chart_minute_ohlcv(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = ChartFuturesOrOptionsData.get_field_aliases(),
    ) -> int:
        """
        Provides access to futures chart data.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for chart data.

        fields :
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.futures_chart_minute_ohlcv(
                symbols=["/ES"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.chart(
            service=ChartServices.CHART_FUTURES.value, symbols=symbols, fields=fields
        )

    def futures_unsub_chart(self):
        """
        Unsubscribe from futures chart service.

        Returns
        ----
        int
            Request number
        """
        if (
            ChartServices.CHART_FUTURES.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(ChartServices.CHART_FUTURES.value)

    # CHART - CHART_OPTIONS
    def options_chart_minute_ohlcv(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = ChartFuturesOrOptionsData.get_field_aliases(),
    ) -> int:
        """
        Provides access to options chart data.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for chart data.

        fields :
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.options_chart_minute_ohlcv(
                symbols=["MSFT_043021C120"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.chart(
            service=ChartServices.CHART_OPTIONS.value, symbols=symbols, fields=fields
        )

    def options_unsub_chart(self):
        """
        Unsubscribe from options chart service.

        Returns
        ----
        int
            Request number
        """
        if (
            ChartServices.CHART_OPTIONS.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(ChartServices.CHART_OPTIONS.value)

    # CHART HISTORY
    def chart_history(
        self,
        service: str | Enum,
        symbol: List[str] | str,
        frequency: str | ChartFuturesFrequencies,
        period: str | ChartFuturesPeriods = None,
        start_time: int | datetime | date = None,
        end_time: int | datetime | date = None,
    ) -> int:
        """
        Stream historical futures prices for charting. For normal equity charts, please use the
        the `get_historical_prices` method.

        Parameters
        ---

        service: str | Enum
            The type of Chart History Service you wish to recieve.
            Only Futures history avilable via streaming server.
            `CHART_HISTORY_FUTURES`

        symbol : List[str] | str
            The symbol for which you want to stream quotes.

        frequency: str | ChartFuturesFrequencies
            The frequency at which you want the data to appear.

        period: str | ChartFuturesPeriods, (optional, Default=None)
            The period you wish to return historical data for. Not
            required if `start_time` or `end_time` is set.

        start_time: int | datetime | date, (optional, Default=None)
            Start time of chart in milliseconds since Epoch, datetime or date.

        end_time: int | datetime | date, (optional, Default=None)
            End time of chart in milliseconds since Epoch, datetime or date.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.chart_history_futures(
                symbol=["/ES"],
                frequency=ChartFuturesFrequencies.ONE_MINUTE,
                period=ChartFuturesPeriods.ONE_DAY
            )

        Note
        ----
        This only accepts one symbol at a time.

        Returns
        ----
        int
            Request number
        """

        # Handle datetimes.
        start_time = convert_to_unix_time_ms(start_time)
        end_time = convert_to_unix_time_ms(end_time)

        if isinstance(frequency, Enum):
            frequency = frequency.value

        if isinstance(period, Enum):
            period = period.value

        # define the valid inputs.
        valid_frequencies = ChartFuturesFrequencies.all_values()
        valid_periods = ChartFuturesPeriods.all_values()

        # validate the frequency input.
        if frequency not in valid_frequencies:
            raise ValueError(
                f"FREQUENCY {frequency} is incorrect choose a valid option:{valid_frequencies}"
            )

        # validate the period input.
        if period not in valid_periods and start_time is None and end_time is None:
            raise ValueError(
                f"PERIOD {period} is incorrect choose a valid option:{valid_periods}"
            )

        request = self.service_helper(service)

        request["command"] = "GET"
        request["parameters"]["frequency"] = frequency
        if isinstance(symbol, list):
            request["parameters"]["symbol"] = ",".join(symbol)
        else:
            request["parameters"]["symbol"] = symbol

        # NOTE: ADD doesn't work, only 1 symbol per sub, but it's documented it should
        if service in self.stream_client.subscribed_services:
            request["command"] = "ADD"
        # handle the case where we get a start time or end time. DO FURTHER VALIDATION.
        if start_time is not None or end_time is not None:
            if start_time is None or end_time is None:
                raise ValueError("Must specify both start and end time")
            request["parameters"]["END_TIME"] = end_time
            request["parameters"]["START_TIME"] = start_time
        else:
            request["parameters"]["period"] = period

        del request["parameters"]["keys"]
        del request["parameters"]["fields"]

        return self.stream_client.add_data_request(request)

    def futures_chart_history(
        self,
        symbol: List[str] | str,
        frequency: str | ChartFuturesFrequencies,
        period: str | ChartFuturesPeriods = None,
        start_time: int | datetime | date = None,
        end_time: int | datetime | date = None,
    ) -> int:
        """
        Stream historical futures prices for charting. For normal equity charts, please use the
        the `get_historical_prices` method.

        Parameters
        ---

        service: str | Enum
            The type of Chart History Service you wish to recieve.
            Only Futures history avilable via streaming server.
            `CHART_HISTORY_FUTURES`

        symbols : List[str] | str
            The symbol for which you want to stream quotes.

        frequency: str | ChartFuturesFrequencies
            The frequency at which you want the data to appear.

        period: str | ChartFuturesPeriods, (optional, Default=None)
            The period you wish to return historical data for. Not
            required if `start_time` or `end_time` is set.

        start_time: int | datetime | date, (optional, Default=None)
            Start time of chart in milliseconds since Epoch, datetime or date.

        end_time: int | datetime | date, (optional, Default=None)
            End time of chart in milliseconds since Epoch, datetime or date.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.futures_chart_history(
                symbols=["/ES"],
                frequency=ChartFuturesFrequencies.ONE_MINUTE,
                period=ChartFuturesPeriods.ONE_DAY
            )

        Note
        ----
        This only accepts one symbol at a time.

        Returns
        ----
        int
            Request number
        """

        return self.chart_history(
            service=ChartHistoryServices.CHART_HISTORY_FUTURES.value,
            symbol=symbol,
            frequency=frequency,
            period=period,
            start_time=start_time,
            end_time=end_time,
        )

    def futures_unsub_chart_history(self):
        """
        Unsubscribe from futures chart history service.

        Returns
        ----
        int
            Request number
        """
        if (
            ChartHistoryServices.CHART_HISTORY_FUTURES.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(ChartHistoryServices.CHART_HISTORY_FUTURES.value)

    # LEVEL ONE - QUOTE
    def level_one_quotes(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelOneEquityData.get_field_aliases(),
    ) -> int:
        """
        Enables Level One streaming quotes.

        Parameters
        ----------
        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields : List[str] | List[int]
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_one_quotes(
                symbols=["AAPL","SQ"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelOneServices.EQUITY.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def equity_unsub_level_one(self) -> int:
        """
        Unsubscribe from equity level one service.

        Returns
        ----
        int
            Request number
        """
        if LevelOneServices.EQUITY.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelOneServices.EQUITY.value)

    # LEVEL ONE - OPTION
    def level_one_options(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelOneOptionData.get_field_aliases(),
    ) -> int:
        """
        Provides access to level one streaming options quotes.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields : List[str] | List[int]
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_one_options(
                symbols=["MSFT_043021C120"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelOneServices.OPTIONS.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def options_unsub_level_one(self) -> int:
        """
        Unsubscribe from options level one service.

        Returns
        ----
        int
            Request number
        """
        if LevelOneServices.OPTIONS.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelOneServices.OPTIONS.value)

    # LEVEL ONE - LEVELONE_FUTURES
    def level_one_futures(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelOneFuturesData.get_field_aliases(),
    ) -> int:
        """
        Provides access to level one streaming futures quotes.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields : List[str] | List[int]
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_one_futures(
                symbols=["/ES"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelOneServices.FUTURES.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def futures_unsub_level_one(self) -> int:
        """
        Unsubscribe from futures level one service.

        Returns
        ----
        int
            Request number
        """
        if LevelOneServices.FUTURES.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelOneServices.FUTURES.value)

    # LEVEL ONE - LEVELONE_FOREX
    def level_one_forex(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelOneForexData.get_field_aliases(),
    ) -> int:
        """
        Provides access to level one streaming forex quotes.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields :
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_one_forex(
                symbols=["EUR/USD"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelOneServices.FOREX.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def forex_unsub_level_one(self) -> int:
        """
        Unsubscribe from forex level one service.

        Returns
        ----
        int
            Request number
        """
        if LevelOneServices.FOREX.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelOneServices.FOREX.value)

    # LEVEL ONE - LEVELONE_FUTURES_OPTIONS
    def level_one_futures_options(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelOneFuturesOptionsData.get_field_aliases(),
    ) -> int:
        """
        Provides access to level one streaming futures options quotes.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for which you want to stream quotes.

        fields : List[str] | List[int]
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_one_futures(
                symbols=["./EW2J20C2675"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(
            LevelOneServices.FUTURES_OPTIONS.value, symbols, fields
        )
        return self.stream_client.add_data_request(request)

    def futures_options_unsub_level_one(self) -> int:
        """
        Unsubscribe from futures options level one service.

        Returns
        ----
        int
            Request number
        """
        if (
            LevelOneServices.FUTURES_OPTIONS.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(LevelOneServices.FUTURES_OPTIONS.value)

    # NEWS
    def news_headline(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = NewsHeadlineData.get_field_aliases(),
    ) -> int:
        """
        Provides access to streaming News Articles.

        Parameters
        ----
        symbols : List[str]
            The list of symbols for which you want to stream news.

        fields : List[str] | List[int]
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.news_headline(
                symbols=["MSFT", "GOOG", "AAPL"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(NewsServices.HEADLINE.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def news_headline_unsub(self) -> int:
        """
        Unsubscribe from news headline service.

        Returns
        ----
        int
            Request number
        """
        if NewsServices.HEADLINE.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(NewsServices.HEADLINE.value)

    def level_two_quotes(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two Equity Quotes.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelTwoServices.EQUITY.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def equity_unsub_level_two(self) -> int:
        """
        Unsubscribe from equity level two service.

        Returns
        ----
        int
            Request number
        """
        if LevelTwoServices.EQUITY.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelTwoServices.EQUITY.value)

    def level_two_options(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two Options Quotes.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelTwoServices.OPTIONS.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def options_unsub_level_two(self) -> int:
        """
        Unsubscribe from options level two service.

        Returns
        ----
        int
            Request number
        """
        if LevelTwoServices.OPTIONS.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelTwoServices.OPTIONS.value)

    def level_two_nasdaq(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two NASDAQ Quotes.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelTwoServices.NASDAQ.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def nasdaq_unsub_level_two(self) -> int:
        """
        Unsubscribe from nasdaq level two service.

        Returns
        ----
        int
            Request number
        """
        if LevelTwoServices.NASDAQ.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelTwoServices.NASDAQ.value)

    def level_two_futures(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two Futures Quotes.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelTwoServices.FUTURES.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def futures_unsub_level_two(self) -> int:
        """
        Unsubscribe from futures level two service.

        Returns
        ----
        int
            Request number
        """
        if LevelTwoServices.FUTURES.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelTwoServices.FUTURES.value)

    def level_two_futures_options(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two Futures Options Quotes.

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(
            LevelTwoServices.FUTURES_OPTIONS.value, symbols, fields
        )
        return self.stream_client.add_data_request(request)

    def futures_options_unsub_level_two(self) -> int:
        """
        Unsubscribe from futures options level two service.

        Returns
        ----
        int
            Request number
        """
        if (
            LevelTwoServices.FUTURES_OPTIONS.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(LevelTwoServices.FUTURES_OPTIONS.value)

    def level_two_forex(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = LevelTwoQuotes.all_values(),
    ) -> int:
        """
        Stream Level Two Forex Quotes.

        Parameters
        ---
        symbols : List[str]
            The list of symbols you want level two data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.level_two_forex(
                symbols=["EUR/USD"]
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(LevelTwoServices.FOREX.value, symbols, fields)
        return self.stream_client.add_data_request(request)

    def forex_unsub_level_two(self) -> int:
        """
        Unsubscribe from forex level two service.

        Returns
        ----
        int
            Request number
        """
        if LevelTwoServices.FOREX.value not in self.stream_client.subscribed_services:
            return
        return self.unsubscribe(LevelTwoServices.FOREX.value)

    def timesale(
        self,
        service: str | TimesaleServices,
        symbols: List[str],
        fields: List[str] | List[int],
    ) -> int:
        """
        Stream Time & Sales Data.

        Parameters
        ---
        service: str | Enum
            The different timesale services, can be `TIMESALE_EQUITY`,
            `TIMESALE_OPTIONS`, `TIMESALE_FUTURES`.

        symbols : List[str]
            The list of symbols you want timesale data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.timesale(
                service=TimesaleServices.TimesaleEquity,
                symbols=["MSFT", "GOOG", "AAPL"],
                fields=Timesale.All
            )

        Returns
        ----
        int
            Request number
        """
        request = self.service_helper(service, symbols, fields)
        return self.stream_client.add_data_request(request)

    def equity_timesale(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = TimesaleData.get_field_aliases(),
    ) -> int:
        """
        Stream Equity Time & Sales Data.

        Parameters
        ---
        symbols : List[str]
            The list of symbols you want timesale data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.equity_timesale(
                symbols=["MSFT", "GOOG", "AAPL"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.timesale(
            service=TimesaleServices.TIMESALE_EQUITY, symbols=symbols, fields=fields
        )

    def equity_unsub_timesale(self) -> int:
        """
        Unsubscribe from equity timesale service.

        Returns
        ----
        int
            Request number
        """
        if (
            TimesaleServices.TIMESALE_EQUITY.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(TimesaleServices.TIMESALE_EQUITY.value)

    def forex_timesale(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = TimesaleData.get_field_aliases(),
    ) -> int:
        """
        Stream Forex Time & Sales Data.

        Parameters
        ---
        symbols : List[str]
            The list of symbols you want timesale data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.forex_timesale(
                symbols=["MSFT", "GOOG", "AAPL"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.timesale(
            service=TimesaleServices.TIMESALE_FOREX, symbols=symbols, fields=fields
        )

    def forex_unsub_timesale(self) -> int:
        """
        Unsubscribe from forex timesale service.

        Returns
        ----
        int
            Request number
        """
        if (
            TimesaleServices.TIMESALE_FOREX.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(TimesaleServices.TIMESALE_FOREX.value)

    def futures_timesale(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = TimesaleData.get_field_aliases(),
    ) -> int:
        """
        Stream Futures Time & Sales Data.

        Parameters
        ---
        symbols : List[str]
            The list of symbols you want timesale data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.futures_timesale(
                symbols=["MSFT", "GOOG", "AAPL"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.timesale(
            service=TimesaleServices.TIMESALE_FUTURES, symbols=symbols, fields=fields
        )

    def futures_unsub_timesale(self) -> int:
        """
        Unsubscribe from futures timesale service.

        Returns
        ----
        int
            Request number
        """
        if (
            TimesaleServices.TIMESALE_FUTURES.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(TimesaleServices.TIMESALE_FUTURES.value)

    def options_timesale(
        self,
        symbols: List[str],
        fields: List[str] | List[int] = TimesaleData.get_field_aliases(),
    ) -> int:
        """
        Stream Options Time & Sales Data.

        Parameters
        ---
        symbols : List[str]
            The list of symbols you want timesale data for.

        fields List[str] | List[int]:
            The data fields to be returned from the endpoint. Can be numeric or string value representations.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> stream_services.options_timesale(
                symbols=["MSFT", "GOOG", "AAPL"]
            )

        Returns
        ----
        int
            Request number
        """
        return self.timesale(
            service=TimesaleServices.TIMESALE_OPTIONS, symbols=symbols, fields=fields
        )

    def options_unsub_timesale(self) -> int:
        """
        Unsubscribe from options timesale service.

        Returns
        ----
        int
            Request number
        """
        if (
            TimesaleServices.TIMESALE_OPTIONS.value
            not in self.stream_client.subscribed_services
        ):
            return
        return self.unsubscribe(TimesaleServices.TIMESALE_OPTIONS.value)

    def unsubscribe(self, service: str | Enum):
        """
        Unsubscribe to service.

        Parameters
        ---
        service: str | Enum
            The service you want to unsubscribe from.

        Returns
        ----
        int
            Request number
        """
        if isinstance(service, Enum):
            service = service.value

        # Build the request
        request = self.new_request_template()
        request["service"] = service
        request["command"] = "UNSUBS"
        return self.stream_client.add_data_request(request)

    def add_handler(self, response_type: str, service: str | Enum, func_):
        """
        Adds a callback handler for a given response type and service.


        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> duration = ActivesDurations.ALL.value
            >>> stream_services.add_handler(
                "data",
                ActivesServices.ACTIVES_NYSE,
                lambda msg: actives_handler.data_message_handler(duration, msg)
            )
        """
        if isinstance(service, Enum):
            service = service.value

        self.stream_client.add_handler(response_type, service, func_)

    def remove_handler(self, response_type: str, service: str | Enum, func_):
        """
        Removes a callback handler for a given response type and service.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> duration = ActivesDurations.ALL.value
            >>> stream_services.remove_handler(
                "data",
                ActivesServices.ACTIVES_NYSE,
                func_ref
            )
        """
        if isinstance(service, Enum):
            service = service.value

        self.stream_client.remove_handler(response_type, service, func_)

    def has_handler(self, response_type: str, service: str | Enum, func_):
        """
        Removes a callback handler for a given response type and service.

        Usage
        ----
            >>> stream_client = td_client.streaming_api_client()
            >>> stream_services = stream_client.services
            >>> duration = ActivesDurations.ALL.value
            >>> stream_services.remove_handler(
                "data",
                ActivesServices.ACTIVES_NYSE,
                func_ref
            )
        """
        if isinstance(service, Enum):
            service = service.value

        self.stream_client.has_handler(response_type, service, func_)

    def is_subscribed(self, service: str | Enum):
        """
        Are you subscribed to given service.

        Parameters
        ---
        service: str | Enum
            The service you want to unsubscribe from.

        Returns
        ----
        int
            Request number
        """
        if isinstance(service, Enum):
            service = service.value
        if service in self.stream_client.subscribed_services:
            return True
        return False
