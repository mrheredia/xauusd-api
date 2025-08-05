# app.py

import random
import os
from flask import Flask, jsonify
import requests

# This is our Flask application instance.
app = Flask(__name__)

# This is our main API endpoint.
@app.route('/xauusd')
def get_xauusd_data():
    """
    Fetches XAUUSD data from a real API, calculates a lot size, TP, and SL
    for both BUY and SELL scenarios, and returns the data as a JSON response.
    """
    # 1. Fetch the live XAUUSD price from the TwelveData API.
    # We now get the API key from a secure environment variable.
    twelvedata_api_key = os.environ.get("TWELVEDATA_API_KEY")
    url = f'https://api.twelvedata.com/quote?symbol=XAU/USD&apikey={twelvedata_api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        current_price_str = data.get('close')
        
        if current_price_str:
            current_price = float(current_price_str)
        else:
            current_price = 2000.00
    
    except requests.exceptions.RequestException:
        current_price = 2000.00

    # 2. Randomize a lot size and a target payout.
    lot_size = round(random.uniform(1.0, 3.0), 2)
    target_payout = random.randint(980, 1160)
    
    # Calculate the required dollar move based on the lot size.
    dollar_move = target_payout / (lot_size * 10)

    # 3. Calculate TP and SL for a BUY trade.
    buy_tp = round(current_price + dollar_move, 2)
    buy_sl = round(current_price - dollar_move, 2)
    
    # 4. Calculate TP and SL for a SELL trade (TP and SL are reversed).
    sell_tp = round(current_price - dollar_move, 2)
    sell_sl = round(current_price + dollar_move, 2)

    # 5. Create a dictionary to hold all our data.
    response_data = {
        "xauusd_price": current_price,
        "lot_size": lot_size,
        "target_payout": target_payout,
        "dollar_move": round(dollar_move, 2),
        "BUY_scenario": {
            "take_profit": buy_tp,
            "stop_loss": buy_sl
        },
        "SELL_scenario": {
            "take_profit": sell_tp,
            "stop_loss": sell_sl
        }
    }

    # 6. Return the dictionary as a JSON response.
    return jsonify(response_data)

if __name__ == '__main__':
    # When deploying, we want to run the app on a port provided by the host.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)