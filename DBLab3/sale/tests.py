from datetime import date
from django.test import TestCase
from sale.models import Product
from sale.models import Customer
from sale.models import Sale
from sale.models import Time


class SaleTestCase(TestCase):
    def setUp(self):
        product = Product.objects.create(name="product_1", category="cat_1", price=123)
        customer = Customer.objects.create(name="Animal", address="meow, 324", phone=234523)
        time = Time.objects.create(date=date(2013, 12, 12), holiday=True, weekend=False)
        sale = Sale.objects.create(customer=customer, product=product, time=time, quantity=12, discount=25,
                                   comment="Hello test!")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        sale = Sale.objects.get(comment="Hello test!")
        self.assertEqual(sale.product.name, 'product_1')

