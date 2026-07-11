import requests

url = "https://official-joke-api.appspot.com/random_joke"

r = requests.get(url)

data = r.json()
print(f" Setup: {data['setup']}")
print(f"Punchline : {data['punchline']}")