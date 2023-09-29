import os
import matplotlib.pyplot as plt
import robin_stocks.robinhood as r
from flask import Flask, jsonify
from pathlib import Path
from dotenv import load_dotenv

master_dict = {}
dotenv_path = Path('ACB/acb.env')
load_dotenv(dotenv_path=dotenv_path)

ROBIN_USER = os.getenv('ROBIN_USER')
ROBIN_PASS = os.getenv('ROBIN_PASS')
r.login(ROBIN_USER, ROBIN_PASS, expiresIn=86400, by_sms=True)

#Look at this horrifying monster of a data structure! - This fetches the pricing info as dictionaries
#deletes irrelevant key/pairs, alters the names of the keys, and updates those keys to the global master_dict
def get_coins():
    # login for Robinhood API, expiresIn is set at the maximum time you can be logged in for before you have to re-authenticate

    btc_info = r.crypto.get_crypto_quote('BTC')
    eth_info = r.crypto.get_crypto_quote('ETH')
    doge_info = r.crypto.get_crypto_quote('DOGE')
    hbar_info = r.crypto.get_crypto_quote('HBAR')

    def delete_keys(coin):
        del coin['ask_price']
        del coin['ask_source']
        del coin['bid_price']
        del coin['bid_source']
        del coin['high_price']
        del coin['low_price']
        del coin['open_price']
        del coin['symbol']
        del coin['id']
        del coin['volume']
        del coin['updated_at']

    delete_keys(btc_info)
    if 'BTC' != 'mark_price':
        btc_info['BTC'] = btc_info['mark_price']
        del btc_info['mark_price']

    delete_keys(eth_info)
    if 'ETH' != 'mark_price':
        eth_info['ETH'] = eth_info['mark_price']
        del eth_info['mark_price']

    delete_keys(doge_info)
    if 'DOGE' != 'mark_price':
        doge_info['DOGE'] = doge_info['mark_price']
        del doge_info['mark_price']

    delete_keys(hbar_info)
    if 'HBAR' != 'mark_price':
        hbar_info['HBAR'] = hbar_info['mark_price']
        del hbar_info['mark_price']

    master_dict.update(hbar_info)
    master_dict.update(doge_info)
    master_dict.update(eth_info)
    master_dict.update(btc_info)


#function that makes a graph of cryptocurrency prices and saves it locally, can adjust size of whole plot figure with "figsize"
def get_plots():
    get_coins()
    cryptocurrency = list(master_dict.keys())
    prices = list(master_dict.values())
    plt.figure(figsize=(15, 5))
    plt.bar(cryptocurrency, prices, width=0.4, color="pink") # width is width of individual bar plot
    plt.xlabel("Cryptocurrencies")
    plt.ylabel("Current Prices")
    plt.savefig('static/test_plots.png')


#flask stuffs
def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.route("/heartbeat")
    def heartbeat():
        return jsonify({"status": "healthy"})

    @app.route("/")
    def catch_all_plots():
        get_plots()
        print('we outcha all day AND night')
        return app.send_static_file('ACB_views.html')

    return app


create_app()
