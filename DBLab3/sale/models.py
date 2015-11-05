from django.db import models
from xml.dom import minidom


class CustomerManager(models.Manager):
    def initialize(self,):
        self.model.objects.all().delete()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE sale_customer AUTO_INCREMENT = 1")
        xmldoc = minidom.parse('tables.xml')
        customer_list = xmldoc.getElementsByTagName('customer')
        for customer in customer_list:
            contactName = str(customer.getElementsByTagName('ContactName')[0].firstChild.data)
            address = str(customer.getElementsByTagName('Address')[0].firstChild.data)
            phone = int(customer.getElementsByTagName('Phone')[0].firstChild.data)
            self.model.objects.create(name=contactName, address=address, phone=phone)


class ProductManager(models.Manager):
    def initialize(self,):
        self.model.objects.all().delete()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE sale_product AUTO_INCREMENT = 1")
        xmldoc = minidom.parse('tables.xml')
        product_list = xmldoc.getElementsByTagName('product')
        for product in product_list:
            productName = str(product.getElementsByTagName('ProductName')[0].firstChild.data)
            categoryName = str(product.getElementsByTagName('CategoryName')[0].firstChild.data)
            productPrice = int(product.getElementsByTagName('ProductPrice')[0].firstChild.data)
            self.model.objects.create(name=productName, category=categoryName, price=productPrice)


class TimeManager(models.Manager):
    def initialize(self,):
        self.model.objects.all().delete()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE sale_time AUTO_INCREMENT = 1")
        xmldoc = minidom.parse('tables.xml')
        time_list = xmldoc.getElementsByTagName('time')
        for time in time_list:
            date = str(time.getElementsByTagName('TheDate')[0].firstChild.data)
            holiday = int(time.getElementsByTagName('Holiday')[0].firstChild.data)
            weekend = int(time.getElementsByTagName('Weekend')[0].firstChild.data)
            self.model.objects.create(date=date, holiday=holiday, weekend=weekend)


class SaleManager(models.Manager):
    def initialize(self,):
        self.model.objects.all().delete()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE sale_sale AUTO_INCREMENT = 1")
        xmldoc = minidom.parse('tables.xml')
        sale_list = xmldoc.getElementsByTagName('sale')
        for sale in sale_list:
            ProductId = int(sale.getElementsByTagName('ProductId')[0].firstChild.data)
            CustomerId = int(sale.getElementsByTagName('CustomerId')[0].firstChild.data)
            TimeId = int(sale.getElementsByTagName('TimeId')[0].firstChild.data)
            LineItemQuantity = int(sale.getElementsByTagName('LineItemQuantity')[0].firstChild.data)
            LineItemDiscount = int(sale.getElementsByTagName('LineItemDiscount')[0].firstChild.data)
            Comment = str(sale.getElementsByTagName('Comment')[0].firstChild.data)
            self.model.objects.create(customer=Customer.objects.get(id=CustomerId),
                                      product=Product.objects.get(id=ProductId), time=Time.objects.get(id=TimeId),
                                      quantity=LineItemQuantity, discount=LineItemDiscount, comment=Comment)


class Customer(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    phone = models.IntegerField()
    objects = CustomerManager()


class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    price = models.IntegerField()
    objects = ProductManager()


class Time(models.Model):
    date = models.DateField()
    holiday = models.BooleanField()
    weekend = models.BooleanField()
    objects = TimeManager()


class Sale(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    time = models.ForeignKey(Time)
    quantity = models.IntegerField()
    discount = models.IntegerField()
    comment = models.TextField()
    objects = SaleManager()


