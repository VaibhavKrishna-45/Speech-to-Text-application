"""Gradio interface and event handlers."""
import gradio as gr

from .logger import get_logger
from .transcription import transcribe_audio

logger = get_logger(__name__)


def _transcribe(audio_path: str | None, language: str, source: str) -> tuple[str, str, str]:
    logger.info("%s transcription requested", source)
    try:
        return transcribe_audio(audio_path, language or None)
    except Exception:
        # Keep the Gradio callback from failing without updating the outputs.
        logger.exception("Unexpected error in %s submission handler", source)
        return "", "Unavailable", "An unexpected error stopped transcription. See logs/application.log for details."


def _transcribe_upload(audio_path: str | None, language: str) -> tuple[str, str, str]:
    return _transcribe(audio_path, language, "Uploaded audio")


def _transcribe_microphone(audio_path: str | None, language: str) -> tuple[str, str, str]:
    return _transcribe(audio_path, language, "Microphone recording")


def build_interface() -> gr.Blocks:
    with gr.Blocks(title="Speech-to-Text Converter") as demo:
        gr.Markdown("# Speech-to-Text Converter\nUpload an audio file or record speech, then transcribe it with Faster-Whisper.")
        with gr.Row():
            # Keep the uploaded file in its original container. Gradio needs
            # FFmpeg to convert formats such as MP3/M4A to WAV; Faster-Whisper
            # can decode the supported formats itself through PyAV.
            audio_file = gr.Audio(label="Audio file", sources=["upload"], type="filepath", format=None)
            microphone = gr.Audio(label="Microphone recording", sources=["microphone"], type="filepath", format="wav")
        language = gr.Dropdown(
            choices=[("Auto detect", ""), ("English", "en"), ("Spanish", "es"), ("French", "fr"),
                     ("German", "de"), ("Hindi", "hi"), ("Japanese", "ja"), ("Chinese", "zh")],
            value="", label="Language", info="Choose Auto detect or specify the spoken language.",
        )
        with gr.Row():
            transcribe_file = gr.Button("Transcribe uploaded audio", variant="primary")
            transcribe_mic = gr.Button("Transcribe recording", variant="primary")
            clear = gr.Button("Clear")
        transcript = gr.Textbox(label="Transcription", lines=10, interactive=False)
        detected = gr.Textbox(label="Detected language", interactive=False)
        status = gr.Textbox(label="Status", interactive=False)
        transcribe_file.click(_transcribe_upload, [audio_file, language], [transcript, detected, status], show_progress="full")
        transcribe_mic.click(_transcribe_microphone, [microphone, language], [transcript, detected, status], show_progress="full")
        clear.click(lambda: (None, None, "", "", ""), outputs=[audio_file, microphone, transcript, detected, status])
    return demo
