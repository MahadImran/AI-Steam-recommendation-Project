import json
from voice_test import model # Reuse the Whisper model from your other script
from brain import recommend_games

def run_app():
    # 1. Voice to Text
    print("\n--- Listening to test.mp3 ---")
    segments, _ = model.transcribe("test.mp3", beam_size=5)
    user_text = "".join([s.text for s in segments])
    print(f"You said: {user_text}")

    # 2. Match with Cache
    with open("games_cache.json", "r") as f:
        cache = json.load(f)

    # 3. Simple Search
    print("\n--- Recommendations ---")
    found = False
    user_text = user_text.lower()
    
    for game in cache:
        # Check if any tag (like 'action') is in what you said
        for tag in game['tags']:
            if tag in user_text:
                print(f"🎯 Match Found: {game['name']}")
                print(f"🔗 Link: {game['link']}")
                print(f"📝 Why: It has the tag '{tag}' which you mentioned.")
                found = True
                break
        if found: break # Just show the top match for now

    if not found:
        print("🤷 No exact matches found in the top trending games.")

if __name__ == "__main__":
    run_app()