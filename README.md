# 👁️ VisionGuide AI

Hands-free, voice-controlled scene description for blind and visually impaired users. Say **"describe"** and get an instant spoken summary of your surroundings — no screen interaction required.

**Live app:** https://visionguide-ai.onrender.com
**Demo video:** [Watch here](YOUR_YOUTUBE_LINK)

## Problem

Visually impaired users often can't rely on touchscreens or visual UI to get help understanding their environment in the moment. Existing tools require manual photo capture and reading results on-screen — both barriers for a blind user.

## Solution

VisionGuide AI is a fully voice-driven web app:
1. Camera starts automatically, app listens for the word **"describe"**
2. On trigger, it captures a frame and sends it to a vision-language model (via Groq)
3. The AI returns Scene / Objects / Safety hazards / Suggested action
4. The result is **spoken aloud** automatically — no reading required
5. Saying "describe" again on the result page loops back for another capture

## Features

- 🎤 Hands-free voice trigger ("describe") using Web Speech API
- 🔊 Automatic text-to-speech readout of results
- 📷 Manual fallback button for browsers without speech recognition (e.g. iOS Safari)
- ⚠️ Structured, safety-focused output: scene, objects, hazards, suggested action
- 🔁 Continuous loop — say "describe" again to analyze a new scene without touching the screen
- 📳 Haptic feedback (vibration) on capture and result-ready events
- 🖥️ Screen Wake Lock to keep voice recognition alive during use

## Tech Stack

- **Backend:** Flask (Python)
- **AI Vision:** Groq API (Qwen vision-language model)
- **Frontend:** Vanilla JS, Web Speech API (SpeechRecognition + SpeechSynthesis), MediaDevices/Canvas
- **Deployment:** Render

## Project Structure

```
vision-assistant/
├── app.py              # Flask routes
├── ai_helper.py         # Groq API integration
├── requirements.txt
├── templates/
│   ├── index.html        # Camera + voice capture UI
│   └── result.html        # Spoken result + voice loop
└── static/
    ├── css/style.css
    └── uploads/            # Captured images (runtime, gitignored)
```

## Installation (local)

```bash
git clone https://github.com/pr-an-a/vision-assistant.git
cd vision-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python app.py
```
Visit `http://localhost:5000`.

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key from [console.groq.com](https://console.groq.com) |

## Future Improvements

- Offline/on-device fallback model for low-connectivity use
- Multi-language voice support
- Distance/obstacle estimation via depth cues
- Native mobile app for reliable background mic access

## Acknowledgements

Built using the Groq API for fast vision-language inference.
