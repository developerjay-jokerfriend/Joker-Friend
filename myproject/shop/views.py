from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil

import json




# Create your views here.
def index(request):
	allProds = []
	category = []
	catprods = Product.objects.values('category', 'id')
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)

		
	cats = {item['category'] for item in catprods} 
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		
		prod=list(prod)
		prod.reverse()
		
		allProds.append([prod, range(1, nSlides), nSlides,n])
	dic = {'allProds':allProds, 'category':category}
	return render(request, 'shop/shop.html',dic)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
    	return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
	return render(request, 'shop/about.html')

def contact(request):
	thank = False
	if request.method=="POST":
		name = request.POST.get('name', '')
		email = request.POST.get('email', '') 
		phone = request.POST.get('phone', '')
		subject = request.POST.get('subject','')
		desc = request.POST.get('desc', '')
		contact = Contact(name=name, email=email, phone=phone,subject=subject, desc=desc)
		contact.save()
		thank = True

	category = []
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)
	dic={'category':category,'thank': thank}
	return render(request, 'shop/contact.html', dic)

def tracker(request):
	category = []
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)
	dic={'category':category,}

	if request.method=="POST":
		orderId = request.POST.get('orderId', '')
		email = request.POST.get('email', '')
		try:
			order = Orders.objects.filter(order_id=orderId, email=email)
			if len(order)>0:
				update = OrderUpdate.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp})
					response = json.dumps([updates, order[0].items_json], default=str)
				return HttpResponse(response, dic)
			else:
				return HttpResponse('{}', dic)
		except Exception as e:
			return HttpResponse('{}', dic)
	return render(request, 'shop/tracker.html', dic)



def search(request):
	return render(request, 'shop/search.html')



def checkout(request):
	category = []
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)

	if request.method=="POST":
		items_json = request.POST.get('itemsJson', '')
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
		city = request.POST.get('city', '')
		state = request.POST.get('state', '')
		pincode = request.POST.get('pincode', '')
		phone = request.POST.get('phone', '')
		order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
			state=state, pincode=pincode, phone=phone)
		order.save()
		update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
		update.save()
		thank = True
		idd = order.order_id
		return render(request, 'shop/checkout.html', {'thank':thank, 'id': idd, 'category': category})
	return render(request, 'shop/checkout.html',{'category': category})