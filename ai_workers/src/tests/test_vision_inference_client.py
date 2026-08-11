from pathlib import Path

import httpx
import pytest

from src.clients.vision_inference_client import (
    RemoteVisionInferenceClient,
    VisionInferenceClientError,
    validate_endpoint_url,
    validate_prediction,
)
from src.pipelines.vision_pipeline import build_vision_predictor


def test_remote_vision_client_posts_image(monkeypatch, tmp_path):
    image_path = tmp_path / "sample.jpg"
    image_path.write_bytes(b"image")
    captured = {}

    def fake_post(url, *, files, headers, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["timeout"] = timeout
        assert files["file"][0] == "sample.jpg"
        return httpx.Response(
            200,
            json={
                "label": "authentic",
                "confidence": 0.8,
                "probabilities": [0.8, 0.2],
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    client = RemoteVisionInferenceClient(
        endpoint_url="https://modal.example/predict",
        api_token="secret",
        timeout_seconds=12,
    )

    result = client.predict(image_path)

    assert captured == {
        "url": "https://modal.example/predict",
        "headers": {"Authorization": "Bearer secret"},
        "timeout": 12,
    }
    assert result["label"] == "authentic"
    assert result["model"]["name"] == "MediaForge Vision"


def test_remote_vision_client_requires_endpoint(monkeypatch):
    monkeypatch.delenv("MODAL_VISION_ENDPOINT_URL", raising=False)

    with pytest.raises(VisionInferenceClientError, match="MODAL_VISION_ENDPOINT_URL"):
        RemoteVisionInferenceClient()


def test_remote_vision_client_rejects_modal_dashboard_url():
    with pytest.raises(VisionInferenceClientError, match="dashboard URL"):
        validate_endpoint_url(
            "https://modal.com/apps/richamgupta2005/main/deployed/"
            "mediaforge-vision/predict"
        )


def test_remote_vision_client_requires_predict_endpoint():
    with pytest.raises(VisionInferenceClientError, match="/predict"):
        validate_endpoint_url("https://example.modal.run")


def test_validate_prediction_rejects_missing_fields():
    with pytest.raises(VisionInferenceClientError, match="missing"):
        validate_prediction({"label": "authentic"})


def test_build_vision_predictor_uses_modal_provider(monkeypatch):
    monkeypatch.setenv("VISION_INFERENCE_PROVIDER", "modal")
    monkeypatch.setenv("MODAL_VISION_ENDPOINT_URL", "https://modal.example/predict")

    predictor = build_vision_predictor()

    assert isinstance(predictor, RemoteVisionInferenceClient)
