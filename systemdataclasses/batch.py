from datetime import datetime


class Batch:
    def __init__(self, batch_number: str, expiry_date: str):
        if batch_number is None or batch_number == "":
            raise ValueError("Batch number cannot be None or empty")
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Expiry date must be in YYYY-MM-DD format")
        self.batch_number = batch_number
        self.expiry_date = expiry_date

    def __str__(self):
        return (
            f"Batch(batch_number={self.batch_number}, expiry_date={self.expiry_date})"
        )

    def toJson(self):
        return {"batch_number": self.batch_number, "expiry_date": self.expiry_date}


class BatchList:
    def __init__(self):
        self.batches = []

    def add_batch(self, batch: Batch):
        if batch is None:
            raise ValueError("Batch cannot be None")
        self.batches.append(batch)

    def remove_batch(self, batch_number: str):
        self.batches = [
            batch for batch in self.batches if batch.batch_number != batch_number
        ]

    def get_batches(self):
        return self.batches

    def find_batch(self, batch_number: str):
        for batch in self.batches:
            if batch.batch_number == batch_number:
                return batch
        return None

    def toJson(self):
        return [batch.toJson() for batch in self.batches]
