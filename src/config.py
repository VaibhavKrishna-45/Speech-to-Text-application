"""Application settings and project paths."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output" / "transcriptions"
LOG_FILE = LOG_DIR / "application.log"

MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base").lower()
SUPPORTED_MODELS = {"tiny", "base", "small", "medium"}
if MODEL_SIZE not in SUPPORTED_MODELS:
    MODEL_SIZE = "base"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
