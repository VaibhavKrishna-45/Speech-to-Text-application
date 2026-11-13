"""Faster-Whisper model lifecycle, transcription, and result persistence."""
from datetime import datetime
from pathlib import Path
from threading import Lock
import time

from faster_whisper import WhisperModel

from .config import COMPUTE_TYPE, DEVICE, MODEL_SIZE, OUTPUT_DIR
from .logger import get_logger

logger = get_logger(__name__)
_model: WhisperModel | None = None
_model_lock = Lock()


class ModelUnavailableError(RuntimeError):
    """The model could not be loaded, usually because it is not cached or reachable."""


def load_model() -> WhisperModel:
    """Load the configured CPU model once and reuse it for all requests."""
    global _model
    with _model_lock:
        if _model is None:
            logger.info("Loading Faster-Whisper model: %s (%s, %s)", MODEL_SIZE, DEVICE, COMPUTE_TYPE)
            try:
                _model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
            except Exception as error:
                raise ModelUnavailableError(
                    f"The '{MODEL_SIZE}' model is not available locally and could not be downloaded. "
                    "Connect to Hugging Face once to download it, then try again."
                ) from error
            logger.info("Faster-Whisper model loaded")
        return _model


def _save_transcription(text: str, language: str, language_probability: float) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone()
    base_name = f"transcription_{timestamp:%Y%m%d_%H%M%S_%f}"
    path = OUTPUT_DIR / f"{base_name}.txt"
    # Exclusive creation ensures simultaneous requests never overwrite one another.
    with path.open("x", encoding="utf-8") as output_file:
        output_file.write(f"Timestamp: {timestamp.isoformat(timespec='seconds')}\n")
        output_file.write(f"Detected language: {language} (probability: {language_probability:.3f})\n\n")
        output_file.write(text)
        output_file.write("\n")
    return path


def transcribe_audio(audio_path: str | Path, language: str | None = None) -> tuple[str, str, str]:
    """Transcribe an audio file; return transcript, language label, and status."""
    if not audio_path:
        return "", "Not detected", "Please upload or record an audio file first."
    path = Path(audio_path)
    if not path.is_file() or path.stat().st_size == 0:
        logger.warning("Audio input missing or empty")
        return "", "Not detected", "The audio file is empty or unavailable. Please try another recording."

    started = time.perf_counter()
    logger.info("Audio processing started (%s input)", "manual language" if language else "automatic language")
    try:
        model = load_model()
        segments, info = model.transcribe(
            str(path), language=language or None, beam_size=5, vad_filter=True
        )
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        elapsed = time.perf_counter() - started
        detected_language = info.language or "unknown"
        logger.info("Language detected: %s", detected_language)
        logger.info("Transcription completed successfully")
        logger.info("Processing time: %.2f seconds", elapsed)
        if not transcript:
            return "", detected_language, "No speech was detected. Try a clearer or longer recording."
        saved_path = _save_transcription(transcript, detected_language, info.language_probability or 0.0)
        logger.info("Transcription saved: %s", saved_path.name)
        return transcript, detected_language, f"Transcription complete in {elapsed:.2f}s. Saved to {saved_path.name}."
    except ModelUnavailableError as error:
        logger.error("Transcription unavailable because the model could not be loaded: %s", error)
        return "", "Unavailable", str(error)
    except Exception:
        logger.exception("Audio transcription failed")
        return "", "Not detected", "The audio could not be decoded or transcribed. Try a WAV, MP3, M4A, or FLAC file, then check logs/application.log for details."
