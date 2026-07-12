"""Check the value of a US Dollar in your Currency"""

import requests
import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()

key = os.getenv("EXCHANGE_KEY")
curr = input("Enter your currency code: ")
try:

    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/USD"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    rate = data['conversion_rates']
    if curr not in rate:
        print(f"{curr} not found")
    else:
        print(f"1 USD: {data['conversion_rates'][curr]} {curr}")



except requests.exceptions.RequestException as e:
    print("Request not found",e)
