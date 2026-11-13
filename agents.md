 Project: Speech-to-Text Application using Faster-Whisper and Gradio

Develop a complete Speech-to-Text application using Python, Gradio, and the Faster-Whisper model.

## 1. Project Objective
Build a user-friendly web application that accepts:
- Audio files uploaded from the local system.
- Live audio recorded through the microphone using Gradio.

The application must convert the speech into text and display the transcription on the Gradio interface.

## 2. Technology Stack
- Python
- Gradio for the web interface.
- Faster-Whisper for speech recognition.
- FFmpeg for audio processing (if required).
- Logging module for application logs.
- Datetime for timestamps.

Install the required packages:

```bash
pip install gradio faster-whisper
```

Use the following model implementation:

```python
from faster_whisper import WhisperModel

model_size = "base"

model = WhisperModel(
    model_size,
    device="cpu",
    compute_type="int8"
)
```

Use CPU execution with INT8 quantization. Keep the model size configurable so it can be changed to tiny, base, small, or medium.

## 3. Application Features

### A. Audio File Upload
- Allow users to upload audio files.
- Support commonly used formats such as WAV, MP3, M4A, and FLAC.
- Process the uploaded audio.
- Convert speech into text.
- Display the complete transcription in a text output area.

### B. Microphone Recording
- Provide a microphone recording option in Gradio.
- Allow users to record their speech directly.
- Process the recorded audio using Faster-Whisper.
- Display the recognized text.

### C. Transcription Features
- Automatically detect the spoken language.
- Display the detected language.
- Display the transcription.
- Include an option to specify a language manually.
- Handle empty audio files and invalid audio gracefully.
- Show a processing indicator while transcription is running.
- Do not crash when audio processing fails.

### D. User Interface
Create a clean and professional Gradio interface containing:
- Application title: Speech-to-Text Converter.
- Audio file upload component.
- Microphone recording component.
- Transcribe button.
- Textbox displaying the transcription.
- Detected language information.
- Clear/reset button.
- Appropriate error messages and status updates.

## 4. Project Folder Structure

Maintain the following structure. Do not put the entire application into one Python file.

```text
SPEECH_TO_TEXT/
│
├── SRC/
│   ├── main.py
│   ├── interface.py
│   ├── transcription.py
│   ├── config.py
│   └── logger.py
│
├── logs/
│   └── application.log
│
├── output/
│   └── transcriptions/
│
├── requirements.txt
├── README.md
└── .gitignore
```

### File Responsibilities

- main.py: Application entry point and Gradio launch.
- interface.py: Gradio UI components and event handling.
- transcription.py: Faster-Whisper model loading and audio transcription logic.
- config.py: Model configuration, paths, and application settings.
- logger.py: Centralized logging configuration.

## 5. Logging System

Implement a proper centralized logging system.

Use Python's built-in logging module.

Requirements:
- Create the logs directory automatically if it does not exist.
- Create application.log automatically.
- Record application startup and shutdown.
- Record audio file uploads.
- Record microphone recording submissions.
- Record transcription start and completion.
- Record detected language.
- Record transcription duration.
- Record errors and exceptions.

Every log entry must contain:
- Date
- Time
- Log level
- Module name
- Meaningful log message

Example:

```text
2026-11-13 15:30:10 | INFO | main | Application started
2026-11-13 15:31:05 | INFO | transcription | Audio processing started
2026-11-13 15:31:08 | INFO | transcription | Language detected: en
2026-11-13 15:31:12 | INFO | transcription | Transcription completed successfully
2026-11-13 15:31:12 | INFO | transcription | Processing time: 4.25 seconds
```

Do not create duplicate logging handlers every time a module is imported.

## 6. Transcription Output Storage

Save each successful transcription as a separate `.txt` file inside:

```text
output/transcriptions/
```

Requirements:
- Automatically generate a unique filename.
- Include the current date and timestamp in the filename.
- Save the transcription text.
- Save the detected language.
- Save the transcription timestamp.
- Do not overwrite previously generated files.

Example:

```text
transcription_20261113_153012.txt
```

## 7. Important Implementation Requirements

- Load the Whisper model only once when the application starts.
- Do not reload the model for every audio submission.
- Keep transcription logic separate from the Gradio interface.
- Use functions and proper exception handling.
- Use pathlib for file and directory management.
- Use meaningful variable and function names.
- Ensure compatibility with Python 3.11.
- Avoid unnecessary dependencies.
- Do not hardcode absolute file paths.
- Ensure uploaded and recorded audio are handled correctly.
- Clean up temporary files when they are no longer required.
- Do not store uploaded audio permanently unless necessary.
- Prevent sensitive information from being unnecessarily exposed in logs.

## 8. README.md

Create a README containing:
- Project description.
- Features.
- Technology stack.
- Installation instructions.
- Virtual environment setup.
- How to run the project.
- Supported audio formats.
- Project folder structure.
- Example usage.

## 9. Requirements.txt

Generate a requirements.txt containing all required dependencies with appropriate version constraints.

## 10. Final Validation

After implementation:

1. Verify that all Python files are connected correctly.
2. Check that all imports work.
3. Verify that the Faster-Whisper model loads successfully.
4. Verify audio file transcription.
5. Verify microphone recording transcription.
6. Verify transcription text is saved in the output folder.
7. Verify logs are generated with timestamps.
8. Verify error handling for invalid audio.
9. Verify that the Gradio application launches successfully.

IMPORTANT:
- Work inside the existing project directory.
- Do not unnecessarily modify or delete existing files.
- If files already exist, inspect them before making changes.
- Do not overwrite existing working functionality without a reason.
- Create missing directories and files automatically.
- Implement the complete working application, not just sample code.
- Fix any errors encountered during implementation.