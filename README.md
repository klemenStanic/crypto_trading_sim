# Crypto trading simulator
A simple crypto trading simulator, which exposes a quart REST api and allows fetching ohlcv data from the okcoin exchange. It also allows to run simple trading simulations.

## How to run
- Create virtualenv:
  ```virtualenv venv```
- Activate virtualenv
  ```source venv/bin/activate```
- Install neccessary packages
  ```pip3 install -r requirements.txt```
- Run script
  ```python3 start.py```

Your Quart server is now running on ```http://localhost:3000```.

# How to use:
Send a GET request to the ```http://localhost:3000/candles``` endpoint with the appended json data.

```bash
curl --location --request GET 'http://localhost:3000/candles' \
--header 'Content-Type: application/json' \
--data-raw '{"start": 1656378000, "end": 1656464400, "interval": "1h", "symbol": "BTC/USDT"}'
```

To run a naive simulation, use the `http://localhost:3000/simulate_trading`:
```bash
curl --location --request POST 'http://localhost:3000/simulate_trading' \
--header 'Content-Type: application/json' \
--data-raw '{"start": 1656378000, "end": 1656064400, "interval": "1h", "symbol": "BTC/USDT"}'
