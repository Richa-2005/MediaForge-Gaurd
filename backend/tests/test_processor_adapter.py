from types import SimpleNamespace

import pytest

from app.services.processor_adapter import process_text_adapter


def test_text_preprocessing_rejects_whitespace(tmp_path):
    path = tmp_path / "blank.txt"
    path.write_text(" \n\t", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        process_text_adapter(SimpleNamespace(id=1, file_path=path))


def test_text_preprocessing_reports_invalid_utf8(tmp_path):
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"\xff\xfe")

    with pytest.raises(ValueError, match="valid UTF-8"):
        process_text_adapter(SimpleNamespace(id=1, file_path=path))
