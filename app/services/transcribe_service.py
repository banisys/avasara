import os

from faster_whisper import WhisperModel

UPLOAD_DIR = "uploads"

model = WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="float32"
)


def transcribe_audio(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    segments, info = model.transcribe(
        file_path,
        language="fa"
    )

    full_text = ""

    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()