import datetime
import calendar
from datetime import date
from django.db.models import Sum, Case, When, F, FloatField
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Category, Transaction
from .serializers import (
    CategorySerializer,
    TransactionReadSerializer,
    TransactionSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TransactionReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None):
        queryset = get_object_or_404(Transaction, id=id)
        serializer = TransactionReadSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        category = request.data.get("category", None)
        if isinstance(category, dict):
            request.data["category"] = category.get("id")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        category = request.data.get("category", None)
        if isinstance(category, dict):
            request.data["category"] = category.get("id")
        serializer = self.get_serializer(instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.delete()
        else:
            return Response(
                {"error": "Tranasaction not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, id=None):
        queryset = get_object_or_404(Category, id=id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            try:
                instance.delete()
            except Exception as e:
                raise Exception(e)
        else:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalyticsViewSet(viewsets.GenericViewSet):
    serializer_class = None
    queryset = Transaction.objects.all()

    def get_last_date_of_current_month(self, start_date):
        today = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        last_day = calendar.monthrange(today.year, today.month)[1]
        last_date = date(today.year, today.month, last_day)
        return last_date

    @action(
        methods=["get"],
        detail=False,
        url_path="transaction/filter",
        url_name="filter-transaction",
    )
    def filter_transactions(
        self,
        request,
    ):
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")
        if not start_date and not end_date:
            start_date = date.today().replace(day=1)
            end_date = date.today()
        elif not end_date:
            end_date = self.get_last_date_of_current_month(start_date)
        data = self._filter_transaction_analytics(start_date, end_date)
        return Response(data)

    @action(
        methods=["get"], detail=False, url_path="transaction", url_name="transaction"
    )
    def get_current_month_transactions(self, request):
        today = date.today()
        start_date = today.replace(day=1)
        end_date = date.today()

        data = self._filter_transaction_analytics(start_date, end_date)
        return Response(data)

    def _filter_transaction_analytics(self, start_date, end_date):
        transactions = Transaction.objects.filter(
            transaction_date__range=(start_date, end_date)
        ).order_by("-amount")
        # Annotate transactions with total amount, considering the transaction type
        transactions = transactions.annotate(
            total_amount=Case(
                When(transaction_type="Income", then=F("amount")),
                default=F("amount") * -1,
                output_field=FloatField(),
            )
        )
        # Calculate total spent amount and group by category
        net_balance = transactions.aggregate(total=Sum("total_amount"))["total"] or 0
        transactions_by_category = (
            transactions.values("category__name")
            .annotate(total_amount=Sum("amount"))
            .order_by("category__name")
        )

        # Calculate income and expense separately
        total_income = (
            transactions.filter(transaction_type="Income").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        total_expense = (
            transactions.filter(transaction_type="Expense").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        # You can further process the data (e.g., group by category)
        data = {
            "transactions": TransactionReadSerializer(
                instance=transactions, many=True
            ).data,
            "balance": float(net_balance),
            "transactions_by_category": list(transactions_by_category),
            "total_income": float(total_income),
            "total_expense": float(total_expense),
        }

        return data
