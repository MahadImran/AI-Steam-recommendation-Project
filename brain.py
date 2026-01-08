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
    with open("games_cache.json", "r") as f:
        cache = json.load(f)

    user_text = user_text.lower()
    scored_games = []

    for game in cache:
        score = 0
        game_tags = game.get('tags', [])

        for tag in game_tags:
            # 1. High weight for what you just said
            if tag in user_text:
                score += 10 
            
            # 2. Add weight from your 'trained' profile
            score += profile['liked_tags'].get(tag, 0)

            # 3. Penalty for things you hate
            if tag in profile.get('disliked_tags', []):
                score -= 20

        if score > 0:
            game['final_score'] = score
            scored_games.append(game)

    # Sort by score so the "best" match is at the top
    scored_games.sort(key=lambda x: x['final_score'], reverse=True)
    return scored_games[:5] # Return top 5

if __name__ == "__main__":
    # Test it with a fake transcription result
    results = recommend_games("I want to play an Action game")
    print(f"Recommended AppIDs: {results}")