from pathlib import Path
import os
from urllib.parse import urlparse

import httpx


AudioInferenceClientError = RuntimeError


class RemoteAudioInferenceClient:
    def __init__(
        self,
        endpoint_url: str | None = None,
        api_token: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.endpoint_url = endpoint_url or os.getenv("MODAL_AUDIO_ENDPOINT_URL", "")
        self.api_token = api_token or os.getenv("MODAL_API_TOKEN", "")
        self.timeout_seconds = timeout_seconds or float(
            os.getenv("AUDIO_INFERENCE_TIMEOUT_SECONDS", "300")
        )

        if not self.endpoint_url:
            raise AudioInferenceClientError(
                "MODAL_AUDIO_ENDPOINT_URL is required when "
                "AUDIO_INFERENCE_PROVIDER=modal."
            )
        validate_endpoint_url(self.endpoint_url)

    def transcribe(self, audio_path: Path) -> dict:
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        try:
            with audio_path.open("rb") as audio_file:
                response = httpx.post(
                    self.endpoint_url,
                    files={
                        "file": (
                            audio_path.name,
                            audio_file,
                            "application/octet-stream",
                        )
                    },
                    headers=headers,
                    timeout=self.timeout_seconds,
                    follow_redirects=True,
                )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AudioInferenceClientError(
                "Remote audio transcription timed out."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise AudioInferenceClientError(
                "Remote audio transcription failed with HTTP status "
                f"{exc.response.status_code}: {exc.response.text[:300]}"
            ) from exc
        except httpx.HTTPError as exc:
            raise AudioInferenceClientError(
                "Remote audio transcription request failed."
            ) from exc

        return validate_transcription(response.json())


def validate_transcription(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise AudioInferenceClientError(
            "Remote audio transcription returned a non-object response."
        )

    if "text" not in payload:
        raise AudioInferenceClientError(
            "Remote audio transcription response is missing: text."
        )

    text = str(payload["text"]).strip()
    language = str(payload.get("language", "unknown") or "unknown")

    return {
        "text": text,
        "language": language,
    }


def validate_endpoint_url(endpoint_url: str) -> None:
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise AudioInferenceClientError(
            "MODAL_AUDIO_ENDPOINT_URL must be a full deployed Modal web "
            "endpoint URL."
        )

    if parsed.netloc == "modal.com" or parsed.netloc.endswith(".modal.com"):
        raise AudioInferenceClientError(
            "MODAL_AUDIO_ENDPOINT_URL is set to a Modal dashboard URL. Use "
            "the deployed Modal web endpoint ending in .modal.run/transcribe."
        )

    if not endpoint_url.rstrip("/").endswith("/transcribe"):
        raise AudioInferenceClientError(
            "MODAL_AUDIO_ENDPOINT_URL should be the deployed transcription "
            "endpoint ending in /transcribe."
        )
