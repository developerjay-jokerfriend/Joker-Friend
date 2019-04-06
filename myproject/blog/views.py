from django.shortcuts import render
from .models import Blogpost
# Create your views here.
from django.http import HttpResponse

def index(request):
    myposts = Blogpost.objects.all()
    myposts = list(myposts)
    myposts.reverse()
    print(myposts)
    return render(request, 'blog/blog.html', {'myposts': myposts})

def blogpost(request, id):
    post = Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return render(request, 'blog/blogpost.html', {'post':post})