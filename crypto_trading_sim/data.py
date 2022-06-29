from dataclasses import InitVar, dataclass, field


@dataclass
class RequestData:
    """
    Data of the request:
    Args:
        start (int): Start of the time range (UTC timestamp)
        end (int): End of the time range (UTC timestamp)
        symbol (str): Trading pair symbol (e.g. BTC/USDT)
        interval (str): Which timeframe to use (e.g. 1m, 1h, 1m, etc.)
    """

    start: int = field(init=False)
    interval: str = field(init=False)
    symbol: str = field(init=False)
    end: int = field(init=False)
    json_data: InitVar[str]

    def __post_init__(self, json_data) -> None:
        self.start = json_data["start"]
        self.end = json_data["end"]
        self.interval = json_data["interval"]
        self.symbol = json_data["symbol"]


@dataclass
class Candle:
    """Wrapper class for data, returned from the exchange."""
    open_time: int = field(init=False)
    close_time: int = field(init=False)
    open: float = field(init=False)
    high: float = field(init=False)
    low: float = field(init=False)
    close: float = field(init=False)
    symbol: str = field(init=False)

    pair_symbol: InitVar[str]
    interval_s: InitVar[int]
    data: InitVar[list]

    def __post_init__(self, pair_symbol, interval_s, data) -> None:
        self.open_time = data[0] // 1000
        self.close_time = data[0] // 1000 + interval_s
        self.open = data[1]
        self.high = data[2]
        self.low = data[3]
        self.close = data[4]
        self.symbol = pair_symbol
