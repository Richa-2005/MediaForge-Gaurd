from pathlib import Path
import os
import shutil
import tempfile

import modal


APP_NAME = "mediaforge-audio"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install("openai-whisper==20250625")
)

app = modal.App(APP_NAME, image=image)


@app.function(
    gpu="T4",
    timeout=10 * 60,
    secrets=[
        modal.Secret.from_name("mediaforge-vision-secrets"),
    ],
)
@modal.asgi_app()
def audio_api():
    from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
    import whisper

    api = FastAPI(title="MediaForge Audio Inference")
    auth_scheme = HTTPBearer(auto_error=False)
    model = whisper.load_model(os.getenv("WHISPER_MODEL_SIZE", "base"))

    def require_token(
        credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
    ) -> None:
        expected_token = os.getenv("MODAL_API_TOKEN", "")
        if not expected_token:
            return
        if credentials is None or credentials.credentials != expected_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid inference token.",
            )

    @api.get("/health")
    def health():
        return {"status": "ok", "service": APP_NAME}

    @api.post("/transcribe")
    async def transcribe(
        file: UploadFile = File(...),
        _auth: None = Depends(require_token),
    ):
        suffix = Path(file.filename or "audio.wav").suffix or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)

        try:
            result = model.transcribe(
                str(temp_path),
                fp16=True,
            )
        finally:
            temp_path.unlink(missing_ok=True)

        text = str(result.get("text", "")).strip()
        return {
            "text": text,
            "language": result.get("language", "unknown"),
        }

    return api
