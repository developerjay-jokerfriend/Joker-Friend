from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact
from math import ceil
# import the logging library

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
	return render(request, 'shop/checkout.html')