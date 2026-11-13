"""Application entry point."""
import logging

from .config import MODEL_SIZE
from .interface import build_interface
from .logger import get_logger
from .transcription import load_model

logger = get_logger("main")


def main() -> None:
    logger.info("Application starting")
    try:
        try:
            load_model()
        except Exception:
            # Keep the interface available when the model has not yet been
            # cached and the machine cannot reach the model host.
            logger.exception("Whisper model could not be loaded; transcription will retry on submission")
        app = build_interface()
        logger.info("Application started")
        app.launch(show_error=False)
    except KeyboardInterrupt:
        logger.info("Application shutdown requested")
    except Exception:
        logger.exception("Application failed to start")
        raise
    finally:
        logger.info("Application shutdown")


if __name__ == "__main__":
    main()
