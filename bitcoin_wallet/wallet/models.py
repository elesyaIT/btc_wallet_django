import uuid
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    """
    Represents a transaction in the system.
    Attributes:
        id (UUIDField): The unique identifier for the transaction.
        amount (DecimalField): The amount of the transaction.
        spent (BooleanField): Indicates whether the transaction has been spent.
        created_at (DateTimeField): The timestamp when the transaction was created.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    spent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transaction {self.id}"
