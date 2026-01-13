import os
from faster_whisper import WhisperModel


model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(file_path):
    print(f"--- Transcribing {file_path} ---")
    segments, info = model.transcribe(file_path, beam_size=5)
    
    print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

if __name__ == "__main__":
   
    if os.path.exists("test.mp3"):
        transcribe_audio("test.mp3")
    else:
        print("❌ Please put a 'test.mp3' file in this folder to test!")
