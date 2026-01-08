import shutil
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from voice_test import model  # Import the model we already tested
import os

from brain import recommend_games

app = FastAPI()

# Tell FastAPI where your HTML and CSS files are
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

import json

import json
import os

# Helper to ensure we always have a profile to read
def get_user_profile():
    profile_path = "user_profile.json"
    if not os.path.exists(profile_path):
        # Default starter profile if none exists
        return {"liked_tags": {}, "disliked_tags": []}
    with open(profile_path, "r") as f:
        return json.load(f)

@app.post("/recommend")
async def get_recommendation(file: UploadFile = File(...)):
    # 1. Save the incoming audio
    temp_filename = "temp_upload.wav"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe
    segments, _ = model.transcribe(temp_filename)
    user_text = " ".join([s.text for s in segments])
    
    # 3. GET THE PROFILE (This fixes the TypeError)
    profile = get_user_profile()
    
    # 4. Get scored recommendations using the profile
    # Now it matches the new recommend_games(user_text, profile) signature
    recommended_games_list = recommend_games(user_text, profile)
    
    # 5. Format for the frontend
    # Since the new brain.py returns full game objects, we can simplify this
    return {
        "transcription": user_text,
        "recommendations": recommended_games_list
    }

@app.post("/like_game")
async def like_game(appid: int):
    with open("games_cache.json", "r") as f:
        cache = json.load(f)
    
    # Find the game and its tags
    tags_to_boost = []
    for game in cache:
        if game['appid'] == appid:
            tags_to_boost = game['tags']
            break

    # Update the profile (The "Training" part)
    with open("user_profile.json", "r+") as f:
        profile = json.load(f)
        for tag in tags_to_boost:
            profile['liked_tags'][tag] = profile['liked_tags'].get(tag, 0) + 1
        
        f.seek(0)
        json.dump(profile, f, indent=4)
        f.truncate()
        
    return {"status": "AI Updated!"}

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 makes it accessible to your other laptop on the same Wi-Fi!
    uvicorn.run(app, host="0.0.0.0", port=8000)