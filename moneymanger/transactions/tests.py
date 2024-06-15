from unicodedata import category
from django.test import TestCase

# Create your tests here.
from datetime import datetime
from django.test.client import Client
from django.urls import reverse

from transactions.models import Category, Transaction

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


