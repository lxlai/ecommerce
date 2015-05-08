from django.conf.urls import url
 
from . import views
 
urlpatterns = [
 url(r'^$', views.index, name='index'),
 url(r'^(?P<item_id>[0-9]+)/$', views.show, name='show'),
 url(r'^cart/(?P<item_id>[0-9]+)/add$', views.purchase_item, name='purchase_item'),
 url(r'^cart$', views.cart, name='cart'),
 url(r'^cart/(?P<item_id>[0-9]+)/delete$', views.delete_item, name='delete_item'),
 url(r'^checkout', views.checkout, name='checkout'),
 url(r'^payments', views.payments, name='payments'),
]