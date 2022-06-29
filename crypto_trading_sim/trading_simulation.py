from abc import ABC, abstractmethod
from data import Candle


class TradingSimulation(ABC):
    """A trading simulation base class."""

    _data: list[Candle]
    _trading_pair: str

    _start_balance_currency_1: float
    _balance_currency_1: float

    _start_balance_currency_2: float
    _balance_currency_2: float

    def __init__(
        self,
        data: list[Candle],
        start_balance_currency_1: float,
        start_balance_currency_2: float,
        trading_pair: str,
    ) -> None:
        self._data = data
        self._start_balance_currency_1 = start_balance_currency_1
        self._start_balance_currency_2 = start_balance_currency_2
        self._trading_pair = trading_pair
        self._balance_currency_1 = start_balance_currency_1
        self._balance_currency_2 = start_balance_currency_2

    def get_results(self, last_candle: Candle) -> dict:
        """Returns results of the simulation."""
        balance_all_start = (
            self._start_balance_currency_1 * last_candle.close
            + self._start_balance_currency_2
        )
        balance_all_end = (
            self._balance_currency_1 * last_candle.close + self._balance_currency_2
        )
        percentage_gain = (
            (balance_all_end - balance_all_start) / balance_all_start
        ) * 100
        return {"gain_percentage": f"{percentage_gain:.2f}"}

    def _sell(self, close_price: float) -> None:
        """Sell the currency at close price"""
        self._balance_currency_2 += self._balance_currency_1 * close_price
        self._balance_currency_1 = 0

    def _buy(self, close_price: float) -> None:
        """Buy the amount of currency at close price"""
        self._balance_currency_1 += self._balance_currency_2 / close_price
        self._balance_currency_2 = 0

    @abstractmethod
    def simulate(self) -> dict:
        """Runs the simulation."""
        pass


class NaiveTradingSimulation(TradingSimulation):
    """A naive trading simulation, using the following rules
    for each time interval:
        if OPEN > CLOSE and have some of the currency, sell at close price
        if OPEN <= CLOSE and have none of the currency, buy at close price
    """

    def __init__(
        self,
        data: list[Candle],
        start_balance_currency_1: float,
        start_balance_currency_2: float,
        trading_pair: str,
    ) -> None:
        super().__init__(
            data=data,
            start_balance_currency_1=start_balance_currency_1,
            start_balance_currency_2=start_balance_currency_2,
            trading_pair=trading_pair,
        )

    def simulate(self) -> dict:
        """Runs the simulation"""
        for candle in self._data:
            if candle.open > candle.close and self._balance_currency_1 > 0:
                self._sell(close_price=candle.close)
            if candle.open <= candle.close and self._balance_currency_1 == 0:
                self._buy(close_price=candle.close)

        last_candle = self._data[-1]
        return self.get_results(last_candle=last_candle)
