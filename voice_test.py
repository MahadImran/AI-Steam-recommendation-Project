import os
from faster_whisper import WhisperModel

# We use 'cuda' to leverage your RTX 4060
# When you move to the 1650, you might change this to 'cpu' if VRAM gets tight
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(file_path):
    print(f"--- Transcribing {file_path} ---")
    segments, info = model.transcribe(file_path, beam_size=5)
    
    print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

if __name__ == "__main__":
    # You need an audio file to test this. 
    # Record yourself saying "I want a multiplayer racing game" and save it as test.mp3
    if os.path.exists("test.mp3"):
        transcribe_audio("test.mp3")
    else:
        print("❌ Please put a 'test.mp3' file in this folder to test!")