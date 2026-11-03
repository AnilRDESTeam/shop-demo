"""Pydantic request models. Responses are plain dicts built in main.py."""
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from app.config import CUSTOM_PRICE_SKU, MAX_CUSTOM_PRICE, MAX_LINES_PER_CART, MAX_QTY_PER_LINE


class CartItem(BaseModel):
    sku: str = Field(min_length=1)
    qty: int = Field(ge=1, le=MAX_QTY_PER_LINE)
    unit_price: Decimal | None = Field(default=None, gt=0, le=MAX_CUSTOM_PRICE, decimal_places=2)

    @model_validator(mode="after")
    def check_custom_price(self):
        # Only TEST-SKU takes a custom price, and it must have one.
        if self.sku == CUSTOM_PRICE_SKU and self.unit_price is None:
            raise ValueError(f"unit_price is required for {CUSTOM_PRICE_SKU}")
        if self.sku != CUSTOM_PRICE_SKU and self.unit_price is not None:
            raise ValueError(f"unit_price is only allowed for {CUSTOM_PRICE_SKU}")
        return self


class CartRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    items: list[CartItem] = Field(min_length=1, max_length=MAX_LINES_PER_CART)
