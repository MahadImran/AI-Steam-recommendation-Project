# AI-Steam-recommendation-Project
(WIP) An AI-powered game recommendation engine that uses OpenAI Whisper for speech-to-text processing and a weighted-scoring algorithm to match user intent with live Steam store data
Steam AI-Voice Recommender
This project provides a hands-on web interface for discovering Steam games through natural language. Instead of clicking through filters, users can simply "speak" their preferences to receive instant, personalized recommendations based on real-time trending data.

Core Features
Voice-to-Intent Processing: Leverages faster-whisper (running locally on CPU/GPU) to transcribe user speech with high accuracy and near-zero latency.

Live Steam Integration: Syncs with the Steam Charts API to maintain a local cache of trending titles, genres, and metadata.

Weighted Recommendation Logic: Uses a scoring engine that analyzes game tags against user-provided keywords.

Dynamic Web Interface: Built with FastAPI and JavaScript to handle asynchronous audio streaming and real-time UI updates.

Personalization (In Development): A profile-based "training" system that adjusts recommendation weights based on user interaction and history.

Tech Stack
Backend: Python 3.13, FastAPI

AI/ML: OpenAI Whisper (faster-whisper)

Frontend: HTML5, CSS3, JavaScript (Web MediaRecorder API)

Data: Steam Store API, JSON-based caching

Environment: Virtual Environments (venv), Dotenv for API security

Why This Project?
This project was developed to explore the intersection of Speech Recognition and Information Retrieval. It demonstrates the ability to:

Integrate multiple third-party APIs.

Optimize AI models for local hardware execution (RTX 4060 vs. CPU).

Handle complex file uploads and binary data (audio blobs) in a web framework.
