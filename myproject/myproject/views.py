# I have created  this views.py file.

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, 'index.html')


def capitalize(request):
	return render(request, 'capitalize.html')

def resultcaps(request):
	rawtext=request.POST.get('caps','default')
	capdone=rawtext.upper()
	dic={'a':capdone}
	return render(request,'resultcaps.html', dic)



