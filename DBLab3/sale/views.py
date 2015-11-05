from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from sale.models import Product
from sale.models import Customer
from sale.models import Sale
from sale.models import Time


def sales_list(request):
    return render(request, 'sales_list.html', {'sales': Sale.objects.all()})


def add_sale(request):
    if request.method == 'POST':
        # db = DB()
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        product = Product.objects.create(name=str(request.POST['ProductName']),
                                         category=str(request.POST['CategoryName']),
                                         price=int(request.POST['ProductPrice']))
        customer = Customer.objects.create(name=str(request.POST['ContactName']),
                                           address=str(request.POST['Address']),
                                           phone=int(request.POST['Phone']))
        time = Time.objects.create(date=str(request.POST['TheDate']),
                                   holiday=int(holiday), weekend=int(weekend))
        Sale.objects.create(customer=customer, product=product, time=time,
                            quantity=int(request.POST['LineItemQuantity']),
                            discount=int(request.POST['LineItemDiscount']),
                            comment=str(request.POST['Comment']))
        return HttpResponseRedirect('/sale/list/')
    sale = None
    return render(request, 'sale_add.html', {'sale': sale})


def search_text(request):
    if request.method == 'POST':
        return render(request, 'sales_list.html',
                      {'sales': Sale.objects.filter(Q(product__name__search=str(request.POST['text'])) | Q(
                          product__category__search=str(request.POST['text'])) | Q(
                          customer__name__search=str(request.POST['text'])) | Q(
                          customer__address__search=str(request.POST['text'])) | Q(
                          comment__search=str(request.POST['text'])))})


def search_integer(request):
    if request.method == 'POST':
        return render(request, 'sales_list.html',
                      {'sales': Sale.objects.filter(Q(product__price__gt=int(request.POST['min_price'])),
                                                    Q(product__price__lt=int(request.POST['max_price'])))})


def search_boolean(request):
    if request.method == 'POST':
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        return render(request, 'sales_list.html',
                      {'sales': Sale.objects.filter(Q(time__holiday=int(holiday)), Q(time__weekend=int(weekend)))})


def remove_sale(request, id_of_sale):
    Sale.objects.get(id=int(id_of_sale)).delete()
    return HttpResponseRedirect('/sale/list/')


def get_sale(request):
    if request.method == 'POST':
        return render(request, 'sale_change.html', {'sale': Sale.objects.get(id=int(request.POST['sale_id']))})
    return render(request, 'sale_get.html', )


def change_sale(request, id_of_sale):
    if request.method == 'POST':
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        sale = Sale.objects.get(id=int(id_of_sale))
        sale.customer.name = str(request.POST['ContactName'])
        sale.customer.address = str(request.POST['Address'])
        sale.customer.phone = int(request.POST['Phone'])
        sale.customer.save()
        sale.product.name = str(request.POST['ProductName'])
        sale.product.category = str(request.POST['CategoryName'])
        sale.product.price = int(request.POST['ProductPrice'])
        sale.product.save()
        sale.time.date = str(request.POST['TheDate'])
        sale.time.holiday = int(holiday)
        sale.time.weekend = int(weekend)
        sale.time.save()
        sale.quantity = int(request.POST['LineItemQuantity'])
        sale.discount = int(request.POST['LineItemDiscount'])
        sale.comment = str(request.POST['Comment'])
        sale.save()
        return HttpResponseRedirect('/sale/list/')
    else:
        sale = Sale.objects.get(id=int(id_of_sale))
    return render(request, 'sale_change.html', {'sale': sale})


def initialization_of_tables(request):
    Customer.objects.initialize()
    Product.objects.initialize()
    Time.objects.initialize()
    Sale.objects.initialize()
    return HttpResponseRedirect('/sale/list/')
