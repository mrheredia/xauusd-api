# app.py

import random
import os
from flask import Flask, jsonify, request  # <-- The 'request' object was missing
import requests

app = Flask(__name__)

# This is the Bin ID from JSONBin.io.
BIN_ID = "6892b8bff7e7a370d1f4e6f9"
API_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"

# The header for making requests to JSONBin.io
HEADERS = {
    "X-Master-Key": os.environ.get("JSONBIN_API_KEY"),
    "Content-Type": "application/json"
}

# New endpoint to receive the price from your local script
@app.route('/update_price', methods=['POST'])
def update_price():
    # Correctly retrieve the JSON data from the request
    data = request.get_json()  # <-- This line has been corrected
    if data and "xauusd_price" in data:
        new_price = data["xauusd_price"]
        
        # Update the price in your JSONBin.io bin
        update_response = requests.put(API_URL, json={"xauusd_price": new_price}, headers=HEADERS)
        update_response.raise_for_status()
        
        return jsonify({"message": "Price updated successfully", "new_price": new_price}), 200
    
    return jsonify({"error": "Invalid data format"}), 400

# Your main API endpoint to serve the data
@app.route('/xauusd')
def get_xauusd_data():
    """
    Fetches XAUUSD data from your JSONBin.io, calculates a lot size, TP, and SL
    for both BUY and SELL scenarios, and returns the data as a JSON response.
    """
    try:
        # Fetch the latest price from your JSONBin.io
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        current_price = data.get("xauusd_price")
        
        if not current_price:
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

    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)