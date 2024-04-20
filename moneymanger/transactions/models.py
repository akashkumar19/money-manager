from uuid import uuid4

from django.db import models


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid4)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Transaction(
    TimeStampedModel
):  # Transaction Model for storing transaction details in database.
    class TransactionType(models.TextChoices):
        INCOME = "Income"
        EXPENSE = "Expense"

    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid4)  # Primary key of the table
    amount = models.DecimalField(decimal_places=2, max_digits=10) # Amount field to store amount of money involved in a particular transaction.
    transaction_date = models.DateTimeField()  # Transaction date field to store exact time when a certain transaction took place.
    transaction_type = models.CharField(
        max_length=10, choices=TransactionType.choices, default=TransactionType.EXPENSE
    )
    note = models.TextField(
        null=True, blank=True
    )  # Note field to store any additional notes related to the particular transaction.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type}-{self.category.name}"
