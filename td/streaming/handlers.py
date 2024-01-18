from abc import ABC

from td.models.streaming import (
    ActivesDataGroup,
    ActivesGroup,
    ActivesSymbol,
    DataResponseMessage,
    SnapshotResponseMessage,
)


class BaseDataMessageHandler(ABC):
    """Abstract base class for data message handlers."""

    def __init__(self, model):
        self.model = model

    def construct_message(self, msg):
        content = msg.get("content", None)

        if content:
            msg["content"] = [self.model(**data) for data in content]
            return DataResponseMessage(**msg)
        return None


class BaseActivesHandler(BaseDataMessageHandler):
    """Handles processing for 'Actives' data messages for ACTIVES_* service."""

    def construct_message(self, msg):
        actives_data_str = msg["content"][0]["1"]
        if len(actives_data_str) > 0:
            actives_data_list = actives_data_str.split(";")
        else:
            return None

        num_groups = int(actives_data_list[4])

        idx = 0 if num_groups == 2 else 4

        def actives_data_helper(group_data):
            group_number = group_data[0]
            num_entries = group_data[1]
            total_volume = int(group_data[2])

            symbols = []
            # Symbols data starts from the 4th entry
            for j in range(3, len(group_data), 3):
                symbol = group_data[j]
                volume = int(group_data[j + 1])
                percent = float(group_data[j + 2])

                symbols.append(
                    ActivesSymbol(symbol=symbol, volume=volume, percent=percent)
                )

            return ActivesGroup(
                group_number=group_number,
                num_entries=num_entries,
                total_volume=total_volume,
                symbol_data=symbols,
            )

        num_trades_active = None
        num_shares_active = None
        group_data = actives_data_list[5 + idx].split(":")
        num_trades_active = actives_data_helper(group_data)

        group_data = actives_data_list[5 + idx + 1].split(":")
        num_shares_active = actives_data_helper(group_data)

        actives_group = ActivesDataGroup(
            group_id=actives_data_list[0],
            sample_duration=int(actives_data_list[1]),
            start_time=actives_data_list[2],
            display_time=actives_data_list[3],
            num_groups=num_groups,
            num_trades_active=num_trades_active,
            num_shares_active=num_shares_active,
        )

        msg["content"][0] = self.model(
            key=msg["content"][0]["key"], actives_data=actives_group
        )
        return DataResponseMessage(**msg), num_trades_active, num_shares_active


class BaseChartHistoryHandler(BaseDataMessageHandler):
    """Base class for CHART_HISTORY service."""

    def construct_message(self, msg):
        if msg.get("content", None):
            # print(f"self.model is {self.model}")
            # print(f"type of msg content{type(msg['content'])}")
            # print(f"len of msg content{len(msg['content'])}")

            # print(f"msg is {msg}")
            # print(f"construct_message msg is {msg}")
            # print(f"first elem of msg content{msg['content'][0]}")

            msg["content"] = [self.model(**data) for data in msg["content"]]
            # print(msg["content"])
            # print("\n\n\n\n\n\n\n")
            # print(msg["content"][0].model_dump(by_alias=True))
            # print("above model_dump second lowest level\n\n\n\n\n\n\n")
            # print(msg["content"][0].data[0].model_dump(by_alias=True))
            # print("above model_dump lowest level\n\n\n\n\n\n\n")

            # temp = SnapshotResponseMessage(**msg)
            # # print(f"temp is {temp}")

            # # print(temp.model_dump(by_alias=True, round_trip=True))
            # # print("above model_dump highest level\n\n\n\n\n\n\n")
            # return temp

            return SnapshotResponseMessage(**msg)
        return None
