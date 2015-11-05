from django.conf.urls import include, url
urlpatterns = [
    url(r'^list/$', 'sale.views.sales_list'),
    url(r'^list/init/$', 'sale.views.initialization_of_tables'),
    url(r'^list/add/$', 'sale.views.add_sale'),
    url(r'^list/remove/(?P<id_of_sale>[0-9]+)/$', 'sale.views.remove_sale'),
    url(r'^list/change/(?P<id_of_sale>[0-9]+)/$', 'sale.views.change_sale'),
    url(r'^list/search/text/$', 'sale.views.search_text'),
    url(r'^list/search/price/$', 'sale.views.search_integer'),
    url(r'^list/search/boolean/$', 'sale.views.search_boolean'),
]


