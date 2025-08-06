# app.py

import random
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Your main API endpoint to serve the data
# The API now expects a 'price' parameter in the URL.
@app.route('/xauusd')
def get_xauusd_data():
    """
    Accepts a 'price' from the URL, calculates a lot size, TP, and SL
    for both BUY and SELL scenarios, and returns the data as a JSON response.
    """
    # Get the price from the URL query parameters
    try:
        current_price_str = request.args.get('price')
        if not current_price_str:
            return jsonify({"error": "Price parameter is missing"}), 400
        current_price = float(current_price_str)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price parameter"}), 400

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

    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)