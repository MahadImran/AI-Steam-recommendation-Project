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

def recommend_games(user_text, profile):
    print(f"--- Analyzing: '{user_text}' ---")
    
    with open("games_cache.json", "r") as f:
        cache = json.load(f)

    user_text = user_text.lower()
    scored_results = []

    for game in cache:
        score = 0
        # 1. Match against current voice command (High Weight: +10)
        for tag in game['tags']:
            if tag in user_text:
                score += 10
            
            # 2. Match against 'trained' profile (Historical Weight)
            score += profile.get("liked_tags", {}).get(tag, 0)

        if score > 0:
            game['score'] = score
            scored_results.append(game)
    
    # Sort by the highest score so the "best" match is first
    scored_results.sort(key=lambda x: x['score'], reverse=True)
    return scored_results[:5]

if __name__ == "__main__":
    # Test it with a fake transcription result
    results = recommend_games("I want to play an Action game")
    print(f"Recommended AppIDs: {results}")