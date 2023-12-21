from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from requests import post
from map.models import MAP
from coments.models import Comment

from django.views.decorators.csrf import csrf_exempt

def index(request):
    id = int(0)
    pages = MAP.objects.all()
    #for page in pages:
     #   print(page.id)
    return render(request, 'base.html',{'pages': pages } )


@csrf_exempt
def next_page(request, idToNewPage, nameOfPage):
    id = int(idToNewPage)
    nameOfPage = nameOfPage
    newPage = MAP(id=id, nameOfPage = nameOfPage)
    newPage.save()
    return redirect('comments:index', idOfPage=id)


#ДОБАВИТЬ КАВЕР 
def newPage(request):
    if request.method == 'POST':
        nameOfPage = request.POST.get('nameOfPage')
        pages = MAP.objects.all()
        max_index = max(pages, key=lambda x: x.id)
        page = MAP(nameOfPage=nameOfPage, id=max_index.id+1)
        page.save()
        pages = MAP.objects.all()
        return redirect('map:index')
    else:
        pages = MAP.objects.all()
        return redirect('map:index')