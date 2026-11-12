from src.ingest.pipeline import normalize_record


def test_normalize_record() -> None:
    rec = normalize_record({"id": "abc", "size": 42})
    assert rec.record_id == "abc"
    assert rec.payload_bytes == 42
