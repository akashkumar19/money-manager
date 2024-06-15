
from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .serializers import TransactionAnalyticsSerializer, TransactionSerializer, CategorySerializer, TransactionReadSerializer
from .models import Transaction, Category
# Create your views here.


class TransactionViewset(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = Transaction.objects.all()
        serializer = TransactionReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, id=None):
        queryset = get_object_or_404(Transaction, id = id)
        serializer = TransactionReadSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        category = request.data.get("category", None)
        if isinstance(category, dict):
            request.data["category"] = category.get('id')
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
            request.data["category"] = category.get('id')
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


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,)
    
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
    

class TransactionAnalyticsView(generics.GenericAPIView):
    serializer_class = TransactionAnalyticsSerializer
    queryset = Transaction.objects.all()

    def get(self, request,): 
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")
        transactions = Transaction.objects.filter(transaction_date__range=(start_date, end_date)) \
                                    .annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at')) \
                                    .values('category__name', 'year', 'month') \
                                    .annotate(total_amount=Sum('amount'))
        total_spent = transactions.aggregate(total=Sum('total_amount'))['total']
        # Calculate percentage for each group
        analyzed_data = [
            {
                'category': transaction['category__name'],
                'year': transaction['year'],
                'month': transaction['month'],
                'total_amount': transaction['total_amount'],
                'percentage': (transaction['total_amount'] / total_spent) * 100
            }
            for transaction in transactions
        ]

        serializer = TransactionAnalyticsSerializer(instance=analyzed_data, many=True)
        return Response(serializer.data)