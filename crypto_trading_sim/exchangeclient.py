import ccxt.async_support as ccxt

from data import Candle, RequestData


class ExchangeClient:
    """
    Client to fetch/post data to the exchange
    :param exchange_id: The ID of an exchange (e.g. binance, okcoin, etc.)
    :returns: None
    :rtype: None
    """

    def __init__(self, exchange_id: str) -> None:
        exchange_class = getattr(ccxt, exchange_id)
        self._ccxt_client = exchange_class()

    async def get_filtered_ohlcv_data(self, request_data: RequestData) -> list:
        """
        Fetches open.high.low.close.volume data from an exchange
        :param request_data: Requested data

        :returns: List of ohlcv values, filtered by using start and end timestamps
        :rtype: list
        """
        interval_s = int(self._ccxt_client.timeframes[request_data.interval])

        res = await self._ccxt_client.fetch_ohlcv(
            symbol=request_data.symbol,
            timeframe=request_data.interval,
            since=request_data.start,
        )

        filtered_parsed_data = [
            Candle(data=el, pair_symbol=request_data.symbol, interval_s=interval_s)
            for el in res
            if el[0] // 1000 + interval_s <= request_data.end
        ]

        print(
            f"Fetched {len(res)} candles. {len(filtered_parsed_data)} were after the requested end time."
        )

        return filtered_parsed_data
