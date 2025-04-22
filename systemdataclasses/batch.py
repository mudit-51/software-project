class Batch:
    def __init__(self, batch_number: str, expiry_date: str):
        self.batch_number = batch_number
        self.expiry_date = expiry_date

    def __str__(self):
        return (
            f"Batch(batch_number={self.batch_number}, expiry_date={self.expiry_date})"
        )
