from pathlib import Path
import os

import httpx


class VisionInferenceClientError(RuntimeError):
    """Raised when the remote vision inference service cannot return a result."""


class RemoteVisionInferenceClient:
    def __init__(
        self,
        endpoint_url: str | None = None,
        api_token: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.endpoint_url = endpoint_url or os.getenv("MODAL_VISION_ENDPOINT_URL", "")
        self.api_token = api_token or os.getenv("MODAL_API_TOKEN", "")
        self.timeout_seconds = timeout_seconds or float(
            os.getenv("VISION_INFERENCE_TIMEOUT_SECONDS", "180")
        )

        if not self.endpoint_url:
            raise VisionInferenceClientError(
                "MODAL_VISION_ENDPOINT_URL is required when "
                "VISION_INFERENCE_PROVIDER=modal."
            )

    def predict(self, image_path: Path) -> dict:
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        try:
            with image_path.open("rb") as image_file:
                response = httpx.post(
                    self.endpoint_url,
                    files={
                        "file": (
                            image_path.name,
                            image_file,
                            "image/jpeg",
                        )
                    },
                    headers=headers,
                    timeout=self.timeout_seconds,
                )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise VisionInferenceClientError(
                "Remote vision inference timed out."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise VisionInferenceClientError(
                "Remote vision inference failed with HTTP status "
                f"{exc.response.status_code}: {exc.response.text[:300]}"
            ) from exc
        except httpx.HTTPError as exc:
            raise VisionInferenceClientError(
                "Remote vision inference request failed."
            ) from exc

        payload = response.json()
        return validate_prediction(payload)


def validate_prediction(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise VisionInferenceClientError(
            "Remote vision inference returned a non-object response."
        )

    missing = {
        key
        for key in ("label", "confidence", "probabilities")
        if key not in payload
    }
    if missing:
        raise VisionInferenceClientError(
            "Remote vision inference response is missing: "
            f"{', '.join(sorted(missing))}."
        )

    label = payload["label"]
    if label not in {"authentic", "manipulated", "uncertain"}:
        raise VisionInferenceClientError(
            f"Remote vision inference returned unsupported label: {label}."
        )

    return {
        "label": label,
        "confidence": float(payload["confidence"]),
        "probabilities": list(payload["probabilities"]),
        "model": payload.get(
            "model",
            {
                "name": "MediaForge Vision",
                "version": "v1",
            },
        ),
    }
