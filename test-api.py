import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("RAWG_API_KEY")

url = "https://api.rawg.io/api/games"

params = {
    "key": api_key,
    "search": "Cyberpunk",
    "page_size": 5,
}

response = requests.get(url, params=params)
data = response.json()

for game in data["results"]:
    print(f"Name: {game['name']}")
    print(f"ID: {game['id']}")
    print(f"Released: {game['released']}")
    print(f"Rating: {game['rating']}")
    print(f"Cover: {game['background_image']}")
    print("--------------------")
