from pydantic import BaseModel


class FeedRecord(BaseModel):
    record_id: str
    payload_bytes: int


def normalize_record(raw: dict[str, object]) -> FeedRecord:
    return FeedRecord(
        record_id=str(raw["id"]),
        payload_bytes=int(raw.get("size", 0)),
    )
