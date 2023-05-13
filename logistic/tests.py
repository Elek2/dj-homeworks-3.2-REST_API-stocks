from django.test import TestCase
# from unittest import TestCase
from rest_framework.test import APIClient


class FirstTestCase(TestCase):
    def test_first(self):
        client = APIClient()
        url = '/api/v1/'
        response = client.get(url)
        self.assertEqual(response.data, 'Hello World!!!')
