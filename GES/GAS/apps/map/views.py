from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from requests import post
from map.models import MAP
from coments.models import Comment

from django.views.decorators.csrf import csrf_exempt

def index(request):
    id = int(0)
    return render(request, 'base.html')


@csrf_exempt
def next_page(request, idToNewPage):
    id = int(idToNewPage)
    newPage = MAP(id=id)
    return redirect('comments:index', idOfPage=id)