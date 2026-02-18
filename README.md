# J.A.R.V.I.S Desktop Assistant

- A Python-based voice assistant built with a hybrid Windows-WSL architecture

## Features

- Voice Recognition: Powered by Google Speech API

- Speech Synthesis: Uses Windows SAPI5 for offline response

- System Monitoring: Real-time battery and power status using 'psutil'

- Desktop automation: Voice commands to launch VS code, chrome and local file directories

- Web Integration: Google searching

## Setup

1. Clone the repo.
2. Install requirements: `pip install -r requirements.txt`.
3. Add your Gemini API Key to a `.env` file.
4. Run `python jarvis_core.py`.
