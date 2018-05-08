from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
    # name = 'NAVI'
    # return HttpResponse('''<h1>Hello {myname} </h1>'''.format(myname=name))
    posts = Post.objects.filter(published_date__lte=timezone.now()).\
                                order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})