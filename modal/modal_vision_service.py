from pathlib import Path
import os
import shutil
import sys
import tempfile

import modal


APP_NAME = "mediaforge-vision"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("libgl1", "libglib2.0-0")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir("ai_workers/src", remote_path="/root/src")
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
def vision_api():
    from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    sys.path.insert(0, "/root")

    from src.processors.mediaforge_predictor import MediaForgePredictor

    api = FastAPI(title="MediaForge Vision Inference")
    auth_scheme = HTTPBearer(auto_error=False)
    predictor = MediaForgePredictor()

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

    @api.post("/predict")
    async def predict(
        file: UploadFile = File(...),
        _auth: None = Depends(require_token),
    ):
        suffix = Path(file.filename or "image.jpg").suffix or ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)

        try:
            prediction = predictor.predict(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        return {
            "label": prediction["label"],
            "confidence": prediction["confidence"],
            "probabilities": prediction["probabilities"],
            "model": {
                "name": "MediaForge Vision",
                "version": "v1",
            },
        }

    return api
