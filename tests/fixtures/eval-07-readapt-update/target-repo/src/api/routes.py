from pydantic import BaseModel


class OrderSummary(BaseModel):
    order_id: str
    total_cents: int


def get_order(order_id: str) -> OrderSummary:
    return OrderSummary(order_id=order_id, total_cents=1250)
