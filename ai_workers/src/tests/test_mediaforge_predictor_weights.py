from pathlib import Path

import pytest

from src.processors import mediaforge_predictor


def test_resolve_weights_path_uses_existing_local_file(
    monkeypatch,
    tmp_path,
):
    weights_path = tmp_path / "mediaforge_vision_v1.pth"
    weights_path.write_bytes(b"weights")

    monkeypatch.setenv(
        "MEDIAFORGE_VISION_WEIGHTS_PATH",
        str(weights_path),
    )

    assert mediaforge_predictor.resolve_weights_path() == weights_path


def test_resolve_weights_path_requires_hf_token_when_missing(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setenv(
        "MEDIAFORGE_VISION_WEIGHTS_PATH",
        str(tmp_path / "missing.pth"),
    )
    monkeypatch.delenv(
        "HF_TOKEN",
        raising=False,
    )

    with pytest.raises(
        mediaforge_predictor.MediaForgeWeightsError,
        match="HF_TOKEN",
    ):
        mediaforge_predictor.resolve_weights_path()


def test_download_weights_uses_private_hf_repo(
    monkeypatch,
    tmp_path,
):
    expected_path = tmp_path / "mediaforge_vision_v1.pth"

    monkeypatch.setenv(
        "HF_TOKEN",
        "hf_test",
    )
    monkeypatch.setenv(
        "MEDIAFORGE_VISION_REPO_ID",
        "rashmijha06/mediaforge_vision",
    )

    def fake_hf_hub_download(
        *,
        repo_id,
        filename,
        token,
        local_dir,
    ):
        assert repo_id == "rashmijha06/mediaforge_vision"
        assert filename == "mediaforge_vision_v1.pth"
        assert token == "hf_test"
        downloaded_path = Path(local_dir) / filename
        downloaded_path.write_bytes(b"weights")
        return str(downloaded_path)

    monkeypatch.setattr(
        mediaforge_predictor,
        "hf_hub_download",
        fake_hf_hub_download,
    )

    assert mediaforge_predictor.download_weights(expected_path) == expected_path
    assert expected_path.read_bytes() == b"weights"
