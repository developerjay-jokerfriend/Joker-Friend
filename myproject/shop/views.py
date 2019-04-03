from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Orders
from math import ceil
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

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



def about(request):
	return render(request, 'shop/about.html')

def contact(request):
	if request.method=="POST":
		name = request.POST.get('name', '')
		email = request.POST.get('email', '') 
		phone = request.POST.get('phone', '')
		subject = request.POST.get('subject','')
		desc = request.POST.get('desc', '')
		contact = Contact(name=name, email=email, phone=phone,subject=subject, desc=desc)
		contact.save()

	category = []
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)
	dic={'category':category,}
	return render(request, 'shop/contact.html', dic)

def tracker(request):
	return render(request, 'shop/tracker.html')

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
		thank = True
		idd = order.order_id
		return render(request, 'shop/checkout.html', {'thank':thank, 'id': idd, 'category': category})
	return render(request, 'shop/checkout.html',{'category': category})