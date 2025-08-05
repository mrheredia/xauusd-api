import MetaTrader5 as mt5
import time
import requests

# This is the public URL of your live Render API.
# You will get this URL from your Render dashboard after we deploy the new code.
API_URL = "https://xauusd-api.onrender.com/update_price"

# Connect to the MT5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

print("Connected to MetaTrader 5 terminal.")

while True:
    try:
        # Get the latest price for XAUUSD
        point_info = mt5.symbol_info_tick("XAUUSD.p")
        current_price = point_info.last

        # Prepare the data to be sent
        payload = {
            "xauusd_price": current_price
        }

        # Send the price to your Render API
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        print(f"Price updated successfully: {current_price}")

    except Exception as e:
        print(f"Error: {e}")

    # Wait for 5 seconds before fetching the price again
    time.sleep(5)