from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'gTzEYqQ8mUAFh42b'




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
	query = request.POST.get('search')
	category = []
	c = Product.objects.values('category')
	for x in c:
		if(x not in category):
			category.append(x)
	
	allProds = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Product.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(query, item)]
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		prod=list(prod)
		prod.reverse()
		if len(prod) != 0:
			allProds.append([prod, range(1, nSlides), nSlides, n])
	dic = {'allProds': allProds, "msg": "", 'category':category}
	if len(allProds) == 0 or len(query)<4:
		dic = {'msg': "Please make sure to enter relevant search query", 'category':category}
	return render(request, 'shop/search.html', dic)



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
		amount = request.POST.get('amount', '')
		email = request.POST.get('email', '')
		address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
		city = request.POST.get('city', '')
		state = request.POST.get('state', '')
		pincode = request.POST.get('pincode', '')
		phone = request.POST.get('phone', '')
		order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
			state=state, pincode=pincode, phone=phone, amount=amount)
		order.save()
		update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
		update.save()
		thank = True
		idd = order.order_id
		#return render(request, 'shop/checkout.html', {'thank':thank, 'id': idd, 'category': category})
		# Request paytm to transfer the amount to your account after payment by user
		param_dict = {
                'MID': 'xeULwa80754021038299',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return render(request, 'shop/paytm.html', {'param_dict': param_dict})


	return render(request, 'shop/checkout.html',{'category': category})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})