import json
import requests

def get_game_tags(appid):
    # This fetches the 'genres' and 'categories' from the Steam store
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        data = requests.get(url).json()
        if data[str(appid)]['success']:
            genres = [g['description'].lower() for g in data[str(appid)]['data'].get('genres', [])]
            return genres
    except:
        return []
    return []

def recommend_games(user_text):
    print(f"--- Analyzing: '{user_text}' ---")
    
    # Load your local cache from Step 4
    with open("games_cache.json", "r") as f:
        trending_games = json.load(f)

    user_text = user_text.lower()
    matches = []

    # Check the first 10 trending games for a match (to keep it fast)
    for game in trending_games[:10]:
        tags = get_game_tags(game['appid'])
        # Simple Logic: If a keyword like 'action' is in your speech and the tags
        for tag in tags:
            if tag in user_text:
                matches.append(game['appid'])
                break
    
    return matches

if __name__ == "__main__":
    # Test it with a fake transcription result
    results = recommend_games("I want to play an Action game")
    print(f"Recommended AppIDs: {results}")