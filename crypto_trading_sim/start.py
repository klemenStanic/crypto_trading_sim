import datetime
import json
from code import InteractiveConsole
from typing import Dict

import ccxt
from quart import Quart, Request, Response, jsonify, request
from quart.utils import run_sync

from config import Config
from data import RequestData
from exchangeclient import ExchangeClient
from trading_simulation import NaiveTradingSimulation

config = Config()
exchange_client = ExchangeClient(config.EXCHANGE)
app = Quart(__name__)


@app.get("/candles")
async def get_candles() -> Response:
    """
    Get candles endpoint.
    """

    req_json = await request.get_json()
    req_data = RequestData(req_json)

    ohlcv_data = await exchange_client.get_filtered_ohlcv_data(req_data)

    return jsonify(ohlcv_data)


@app.post("/simulate_trading")
async def simulate_trading() -> Response:
    """
    Simulate trading.
    """
    req_json = await request.get_json()
    req_data = RequestData(req_json)

    ohlcv_data = await exchange_client.get_filtered_ohlcv_data(req_data)
    naive_sim = NaiveTradingSimulation(
        data=ohlcv_data,
        start_balance_currency_1=0,
        start_balance_currency_2=40000,
        trading_pair=req_data.symbol,
    )
    result = naive_sim.simulate()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
