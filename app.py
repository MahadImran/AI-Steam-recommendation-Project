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

@app.post("/recommend")
async def get_recommendation(file: UploadFile = File(...)):
    # 1. Save the incoming audio blob from the browser
    temp_filename = "temp_upload.wav"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe using our existing Whisper model
    # We define 'user_text' here so the next step can find it!
    segments, _ = model.transcribe(temp_filename)
    user_text = " ".join([s.text for s in segments])
    
    # 3. Get ID list from our brain.py using the user_text we just made
    recommended_appids = recommend_games(user_text)
    
    # 4. Load the cache to find names and links
    with open("games_cache.json", "r") as f:
        cache = json.load(f)
    
    # 5. Create a list of rich game objects for the website
    rich_results = []
    for appid in recommended_appids:
        for game in cache:
            if game['appid'] == appid:
                rich_results.append({
                    "name": game['name'],
                    "link": game['link'],
                    "tags": game['tags']
                })
                break
                
    return {
        "transcription": user_text,
        "recommendations": rich_results
    }
if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 makes it accessible to your other laptop on the same Wi-Fi!
    uvicorn.run(app, host="0.0.0.0", port=8000)