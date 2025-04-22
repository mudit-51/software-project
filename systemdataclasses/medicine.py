from __future__ import annotations
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    import vendor  # noqa: F401
    import batch


class Medicine:
    def __init__(
        self,
        name: str,
        batch: batch.Batch,
        expiry_date: str,
        price: float,
        vendor: vendor.Vendor,
    ):
        self.name = name
        self.identifier = name.replace(" ", "_").lower() + "_" + str(time.time())
        self.batch = batch
        self.expiry_date = expiry_date
        self.price = price
        self.vendor = vendor

    def __str__(self):
        return f"Medicine(name={self.name}, batch_number={str(self.batch)}, expiry_date={self.expiry_date}, price={self.price}, vendor={self.vendor})"
