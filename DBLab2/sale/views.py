from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from db import DB

def sales_list(request):
    #return HttpResponse('hello, world')
    db = DB()
    sales = db.get_sales_list()

    return render(request, 'sales_list.html', {'sales': sales})


def add_sale(request):
    if request.method == 'POST':
        db = DB()
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        print(holiday, weekend)
        db.save_sale(str(request.POST['ProductName']), str(request.POST['CategoryName']), int(request.POST['ProductPrice']),
                     int(request.POST['LineItemQuantity']), int(request.POST['LineItemDiscount']), str(request.POST['ContactName']),
                     str(request.POST['Address']), int(request.POST['Phone']), str(request.POST['TheDate']),
                     int(holiday), int(weekend), str(request.POST['Comment']),)
        return HttpResponseRedirect('/sale/list/')
    sale = None
    return render(request, 'sale_add.html', {'sale': sale})


def search_text(request):
    if request.method == 'POST':
        db = DB()
        sales = db.search_text(str(request.POST['text']))
        return render(request, 'sales_list.html', {'sales': sales})


def search_integer(request):
    if request.method == 'POST':
        db = DB()
        sales = db.search_integer(int(request.POST['min_price']), int(request.POST['max_price']))
        return render(request, 'sales_list.html', {'sales': sales})


def search_boolean(request):
    if request.method == 'POST':
        db = DB()
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        sales = db.search_boolean(int(holiday), int(weekend))
        return render(request, 'sales_list.html', {'sales': sales})


def remove_sale(request, id_of_sale):
    db = DB()
    db.remove_sale(int(id_of_sale))
    return HttpResponseRedirect('/sale/list/')


def get_sale(request):
    if request.method == 'POST':
        db = DB()
        sale = db.get_sale(int(request.POST['sale_id']), )
        return render(request, 'sale_change.html', {'sale': sale})
    return render(request, 'sale_get.html',)


def change_sale(request, id_of_sale):
    if request.method == 'POST':
        db = DB()
        holiday = 0
        weekend = 0
        if request.POST.get('Holiday'):
            holiday = 1
        if request.POST.get('Weekend'):
            weekend = 1
        db.change_sale(int(id_of_sale), str(request.POST['ProductName']), str(request.POST['CategoryName']), int(request.POST['ProductPrice']),
                       int(request.POST['LineItemQuantity']), int(request.POST['LineItemDiscount']), str(request.POST['ContactName']),
                       str(request.POST['Address']), int(request.POST['Phone']), str(request.POST['TheDate']),
                       int(holiday), int(weekend), str(request.POST['Comment']),)
        return HttpResponseRedirect('/sale/list/')
    else:
        db = DB()
        sale = db.get_sale(int(id_of_sale))
    return render(request, 'sale_change.html', {'sale': sale})


def initialization_of_tables(request):
    db = DB()
    db.initialization()
    return HttpResponseRedirect('/sale/list/')