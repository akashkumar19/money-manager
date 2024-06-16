import calendar
from django.test import TestCase

# Create your tests here.
from datetime import datetime
from django.test.client import Client
from django.urls import reverse

from transactions.views import AnalyticsViewSet
from transactions.models import Category, Transaction
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import date

class TestTransactionViewSet(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.category = Category.objects.create(name="test")
        self.transaction = Transaction.objects.create(amount=500, transaction_date=datetime.now(), transaction_type='Expense', note="test", category=self.category)
        self.url = reverse('transaction-list')

    @property
    def good_post_data(self):
        return {
            "amount": 200,
            "transaction_date": datetime(2024, 6, 5),
            "transaction_type": "Income",
            "category": self.category.id
        }
    
    def test_get_transaction(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['amount']), float(self.transaction.amount))
        self.assertEqual(response.data[0]['note'], self.transaction.note)
        self.assertEqual(response.data[0]['category']['id'], str(self.transaction.category.id))

    def test_create_transaction(self):
        response = self.client.post(self.url, data=self.good_post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(float(response.data['amount']), float(self.good_post_data['amount']))
        self.assertEqual(response.data['category'], self.category.id)

    def test_update_transaction(self):

        url = reverse("transaction-detail", kwargs={"id": self.transaction.id})
        data = self.good_post_data.copy()
        data["amount"] = 300
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.data['amount']), float(300))

    def test_delete_transaction(self):
        url = reverse("transaction-detail", kwargs={"id": self.transaction.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class TestCategoryViewSet(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.category = Category.objects.create(name="test")
        self.url = reverse('category-list')

    @property
    def good_post_data(self):
        return {
            "name": "test create",
            "description": "test-description"
        }
    
    def test_get_category(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_create_category(self):
        response = self.client.post(self.url, data=self.good_post_data)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data['name'], self.good_post_data['name'])
        self.assertEqual(response.data['description'], self.good_post_data['description'])

    def test_update_category(self):

        url = reverse("category-detail", kwargs={"id": self.category.id})
        data = self.good_post_data.copy()
        data["description"] = "updated description"
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], data['description'])

    def test_delete_category(self):
        url = reverse("category-detail", kwargs={"id": self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)




class TestAnalyticsViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name="Food")
        self.category2 = Category.objects.create(name="Transportation")
        self.transaction1 = Transaction.objects.create(
            amount=100,
            transaction_date=date.today(),
            category=self.category1,
            transaction_type="Expense"
        )
        self.transaction2 = Transaction.objects.create(
            amount=50,
            transaction_date=date.today(),
            category=self.category2,
            transaction_type="Expense"
        )
        self.transaction3 = Transaction.objects.create(
            amount=150,
            transaction_date=date.today(),
            category=self.category1,
            transaction_type="Income"
        )

    def test_filter_transactions_with_valid_dates(self):
        """
        Test that the filter_transactions method returns the correct data when valid dates are provided.
        """
        start_date = date.today().replace(day=1)
        end_date = date.today()
        response = self.client.get(reverse('analytics-filter-transaction'), {'start': start_date.isoformat(), 'end': end_date.isoformat()})
        data = response.json()
        self.assertEqual(data['transactions'][0]['category']['name'], 'Food')
        self.assertEqual(data['transactions'][1]['category']['name'], 'Food')
        self.assertEqual(data['balance'], 100 + 50 - 150)

        self.assertEqual(data['transactionsByCategory'][0]['category_Name'], 'Food')
        self.assertEqual(data['transactionsByCategory'][0]['totalAmount'], 250)
        self.assertEqual(data['totalIncome'], 150)
        self.assertEqual(data['totalExpense'], 150)

    def test_get_current_month_transactions(self):
        """
        Test that the get_current_month_transactions method returns the correct data.
        """
        response = self.client.get(reverse('analytics-transaction'))
        data = response.json()
        self.assertEqual(data['transactions'][0]['category']['name'], 'Food')
        self.assertEqual(data['transactions'][1]['category']['name'], 'Food')
        self.assertEqual(data['balance'], 100 + 50 - 150)
        self.assertEqual(data['transactionsByCategory'][0]['category_Name'], 'Food')
        self.assertEqual(data['transactionsByCategory'][0]['totalAmount'], 250)
        self.assertEqual(data['totalIncome'], 150)
        self.assertEqual(data['totalExpense'], 150)

    def test_get_last_date_of_current_month(self):
        """
        Test that the get_last_date_of_current_month method returns the correct date.
        """
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        last_date = date(today.year, today.month, last_day)
        self.assertEqual(AnalyticsViewSet().get_last_date_of_current_month(today.isoformat()), last_date)
