import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")

def fetch_trending_with_tags():
    print("--- Fetching Top Games & Tags ---")
    # 1. Get the trending list
    list_url = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={API_KEY}"
    list_res = requests.get(list_url).json()
    ranks = list_res.get("response", {}).get("ranks", [])[:50] # Let's do top 50

    detailed_games = []
    
    for game in ranks:
        appid = game['appid']
        print(f"Fetching tags for ID: {appid}...")
        
        # 2. Get details (tags/genres) for EACH game
        detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        try:
            res = requests.get(detail_url).json()
            # Inside fetch_trending_with_tags loop
            if res[str(appid)]['success']:
                data = res[str(appid)]['data']
                genres = [g['description'].lower() for g in data.get('genres', [])]
                
                # NEW: Get the short description to help the AI understand the 'vibe'
                short_description = data.get('short_description', '')
                
                detailed_games.append({
                    "appid": appid,
                    "name": data.get('name'),
                    "tags": genres,
                    "description": short_description, # Save the summary!
                    "link": f"https://store.steampowered.com/app/{appid}"
            })
        except:
            continue
        
        # 3. Pause for a second so Steam doesn't block us
        time.sleep(1.5)

    with open("games_cache.json", "w") as f:
        json.dump(detailed_games, f, indent=4)
    print("✅ Done! Cache updated with tags.")

if __name__ == "__main__":
    fetch_trending_with_tags()