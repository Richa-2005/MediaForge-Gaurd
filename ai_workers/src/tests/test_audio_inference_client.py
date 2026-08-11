import httpx
import pytest

from src.clients.audio_inference_client import (
    AudioInferenceClientError,
    RemoteAudioInferenceClient,
    validate_endpoint_url,
    validate_transcription,
)


def test_remote_audio_client_posts_audio(monkeypatch, tmp_path):
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"audio")
    captured = {}

    def fake_post(url, *, files, headers, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["timeout"] = timeout
        assert files["file"][0] == "sample.wav"
        return httpx.Response(
            200,
            json={
                "text": "hello world",
                "language": "en",
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    client = RemoteAudioInferenceClient(
        endpoint_url="https://audio.example.modal.run/transcribe",
        api_token="secret",
        timeout_seconds=12,
    )

    result = client.transcribe(audio_path)

    assert captured == {
        "url": "https://audio.example.modal.run/transcribe",
        "headers": {"Authorization": "Bearer secret"},
        "timeout": 12,
    }
    assert result == {
        "text": "hello world",
        "language": "en",
    }


def test_remote_audio_client_rejects_modal_dashboard_url():
    with pytest.raises(AudioInferenceClientError, match="dashboard URL"):
        validate_endpoint_url(
            "https://modal.com/apps/richamgupta2005/main/deployed/"
            "mediaforge-audio/transcribe"
        )


def test_remote_audio_client_requires_transcribe_endpoint():
    with pytest.raises(AudioInferenceClientError, match="/transcribe"):
        validate_endpoint_url("https://audio.example.modal.run")


def test_validate_transcription_requires_text():
    with pytest.raises(AudioInferenceClientError, match="text"):
        validate_transcription({"language": "en"})
