from django.test import TestCase

# Create your tests here.

class BasicTest(TestCase):
    def test_home(self):
        response = self.client.get('/hofme/')
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_account(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

    def test_cart(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
