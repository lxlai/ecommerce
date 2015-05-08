from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers
from django.core.urlresolvers import reverse
from members.views import User



# Create your views here.

def index(request):

	search = request.GET.get('search')
	price_cat = request.GET.get('filter')
	items_list = Item.objects.all()

	if request.user.is_authenticated():
		name = request.user.first_name
	else:
		name = ''

	# put all this shit into hash
	if price_cat=='1':
		items_list = items_list.filter(price__lte=19.99)

	if price_cat=='2':
		items_list = items_list.filter(price__gte=20, price__lte=39.99)

	if price_cat=='3':
		items_list = items_list.filter(price__gte=40, price__lte=59.99)

	if price_cat=='4':
		items_list = items_list.filter(price__gt=59.99)

	if search:
		items_list = items_list.filter(Q(name__icontains=search) | Q(description__icontains=search))

	paginator = Paginator(items_list, 10)
	page = request.GET.get('page')

	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	if request.GET.get("format")=="json":
		items = serializers.serialize("json",items)
		return HttpResponse(items, content_type='application/json')

	return render_to_response('items/index.html', {'items': items, 'name':name})

def cart(request):
	order=Order.objects.get(user=request.user)
	items=order.items.all()
	total = 0
	for item in items:
		total += item.price
	return render(request, 'items/cart.html', {'items':items, 'total':total})

def purchase_item(request, item_id):
	if request.user.is_authenticated():

		if request.user.order_set.all():
			orders=request.user.order_set.all()

			if orders.filter(status=1):
				order=orders.filter(status=1)[0]
				order.items.add(Item.objects.get(id=item_id))
				return HttpResponseRedirect(reverse('items:cart'))

			# fix redundancy of else statements below
			else:
				order=Order(status=1, user=request.user)
				order.save()
				order.items.add(Item.objects.get(id=item_id))
				return HttpResponseRedirect(reverse('items:cart'))

		else:
			order=Order(status=1, user=request.user)
			order.save()
			order.items.add(Item.objects.get(id=item_id))
		 	return HttpResponseRedirect(reverse('items:cart'))
			
	return HttpResponseRedirect(reverse('members:login'))

def delete_item(request, item_id):
	order=Order.objects.get(user=request.user)
	order.items.remove(Item.objects.get(id=item_id))
	return HttpResponseRedirect(reverse('items:cart'))

def checkout(request):
	return render(request, 'items/checkout.html', {})

def show(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	return render(request, 'items/show.html', {'item': item})
