from rest_framework import serializers

from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "amount",
            "transaction_date",
            "transaction_type",
            "note",
            "category",
        ]


class TransactionReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "transaction_date",
            "transaction_type",
            "note",
            "category",
            "created_at",
            "updated_at",
        ]


class TransactionAnalyticsSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=100)
    year = serializers.IntegerField(required=False)
    month = serializers.IntegerField(required=False)
    total_amount = serializers.DecimalField(max_digits=100, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=100, decimal_places=2)
