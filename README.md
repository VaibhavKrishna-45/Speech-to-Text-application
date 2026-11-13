# Speech-to-Text Converter

A local Gradio application that transcribes uploaded audio and microphone recordings with Faster-Whisper. It runs the configurable Whisper model on CPU with INT8 quantization, detects language automatically (or accepts a selected language), and saves each successful transcript as a timestamped text file.

## Features

- Upload WAV, MP3, M4A, and FLAC audio or record from a microphone.
- Automatic language detection or manual selection.
- Clear status and validation messages for empty, silent, or invalid audio.
- One model instance is loaded at startup and reused.
- Timestamped logs and transcript files are written locally.

## Technology

Python 3.11, Gradio, Faster-Whisper, and Python's built-in logging module. Faster-Whisper uses CTranslate2 for CPU inference; install FFmpeg if your platform needs it for audio decoding.

## Installation

From the project directory, create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate` instead. The first launch downloads the configured model if it is not cached. The default `base` model can be changed using `WHISPER_MODEL_SIZE` to `tiny`, `base`, `small`, or `medium`.

## Run

```powershell
python -m SRC.main
```

Open the local URL printed by Gradio, upload or record audio, optionally choose a language, then click the matching transcribe button. Clear resets the form.

## Supported audio

WAV, MP3, M4A, and FLAC are accepted. Other formats may work depending on the FFmpeg/decoder support available in the environment.

## Project structure

```text
SPEECH-TEXT/
├── SRC/
│   ├── main.py
│   ├── interface.py
│   ├── transcription.py
│   ├── config.py
│   ├── logger.py
│   └── __init__.py
├── logs/application.log       # created at runtime
├── output/transcriptions/     # created as transcripts are saved
├── requirements.txt
├── README.md
└── .gitignore
```
