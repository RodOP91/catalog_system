from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient

from .models import *
from catalog_auth.models import *

class ProductCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AuthToken.objects.create(user=self.user)
        self.token.expires_at = timezone.now() + timezone.timedelta(days=1)
        self.token.save()

    def test_create_product(self):
        # Data to test
        data = {
            'name': 'Test Product',
            'sku': 'TP001',
            'brand':'Brand',
            'price': 9.99,
        }

        # Adding the token
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.token.token}')

        # POST request for product creation
        response = self.client.post('/api/product/', data)
        print(response.content)

        # Asserting request was a success and object is inserted correctly in database
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.sku, data['sku'])
        self.assertAlmostEqual(float(product.price), data['price'], places=2)

class ProductUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AuthToken.objects.create(user=self.user)
        self.token.expires_at = timezone.now() + timezone.timedelta(days=1)
        self.token.save()
        self.product = Product.objects.create(name='Test Product', sku='TP001', price=9.99)

    def test_update_product(self):
        # Data to test
        data = {
            'name': 'Test Product',
            'sku': 'TP100',
            'brand':'NewBrand',
            'price': 0.99,
        }
        # Set the token
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.token.token}')

        # PATCH request for product update
        response = self.client.patch(f'/api/product/{self.product.sku}/', data)

        updated_product = Product.objects.get(sku=data['sku'])

        # Asserting request was a success and object is updated correctly in database
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(updated_product.name, data['name'])
        self.assertEqual(updated_product.brand, data['brand'])
        self.assertEqual(updated_product.sku, data['sku'])
        self.assertAlmostEqual(float(updated_product.price), data['price'], places=2)

class ProductDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AuthToken.objects.create(user=self.user)
        self.token.expires_at = timezone.now() + timezone.timedelta(days=1)
        self.token.save()
        self.product = Product.objects.create(name='Test Product', sku='TP001', price=9.99)

    def test_delete_product(self):
        # Set the authentication header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.token.token}')

        # Send a DELETE request to delete the product
        response = self.client.delete(f'/api/product/{self.product.sku}/')

        # Assert that the response has a 204 status code
        self.assertEqual(response.status_code, 204)

        # Assert that the product was deleted from the database
        self.assertEqual(Product.objects.count(), 0)