from unittest.mock import Mock

import numpy as np

from src.audio_forensics import transcription


def test_transcription_decodes_audio_without_system_ffmpeg(
    monkeypatch,
    tmp_path,
):
    samples = np.zeros(16000, dtype=np.float32)
    load = Mock(return_value=(samples, 16000))
    monkeypatch.setattr(transcription.librosa, "load", load)
    model = Mock()
    model.transcribe.return_value = {
        "text": "sample transcript",
        "language": "en",
    }
    analyzer = transcription.TranscriptionAnalyzer.__new__(
        transcription.TranscriptionAnalyzer
    )
    analyzer.model = model
    path = tmp_path / "sample.mp3"

    result = analyzer.analyze(path)

    load.assert_called_once_with(
        path,
        sr=transcription.whisper.audio.SAMPLE_RATE,
        mono=True,
    )
    assert model.transcribe.call_args.args[0] is samples
    assert result.metadata["transcript"] == "sample transcript"
