import json
import os
from sentence_transformers import SentenceTransformer, util

# Load a lightweight AI model for semantic meaning
# This will download the first time you run it 
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_games(user_text, profile):
    print(f"--- AI Semantic Analysis: '{user_text}' ---")
    
    # Load your local cache created by steam_handler.py
    if not os.path.exists("games_cache.json"):
        return []
        
    with open("games_cache.json", "r") as f:
        cache = json.load(f)

    # 1. Encode the user's voice request into a semantic vector
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    
    scored_results = []

    for game in cache:
        # Combine tags AND the description for much better matching
        # Now the AI will see words like "scary", "terrifying", or "zombies"
        full_metadata = " ".join(game.get('tags', [])) + " " + game.get('description', '')
        
        game_embedding = model.encode(full_metadata, convert_to_tensor=True)
        
        # Semantic similarity score
        semantic_score = util.cos_sim(user_embedding, game_embedding).item()
        
        # 4. Hybrid Layer: Add weight from your 'trained' profile
        profile_bonus = 0
        liked_tags = profile.get("liked_tags", {})
        disliked_tags = profile.get("disliked_tags", []) # Get the dislikes!
        for tag in game.get('tags', []):
            # Scale the bonus so it doesn't completely overwhelm the AI's logic
            profile_bonus += liked_tags.get(tag, 0) * 0.01
            # We also penalize disliked tags
            if tag in disliked_tags:
                profile_bonus -= 0.02  # Penalize disliked tags

        final_score = semantic_score + profile_bonus
        
        # Only keep results that actually make sense
        if final_score > 0.2:
            game['score'] = final_score
            scored_results.append(game)
    
    # Sort by the highest AI + Profile score
    scored_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    return scored_results[:5]
