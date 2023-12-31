from django.shortcuts import render, redirect
from coments.models import Comment
from map.models import MAP
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import page


def index(request, idOfPage):
    
    category = MAP.objects.get(id = idOfPage)

    pages = page.objects.filter(map = category)
    nameOfPage = category.nameOfPage

    print(nameOfPage, pages)
    idOfPage = int(idOfPage)
    return render(request, 'listOfPages.html', {'map_internal_pages': pages, 'nameOfPage' : nameOfPage} )


def openPage(request, idOfPage):

    PAGE = page.objects.get(id = idOfPage)
    nameOfPage = PAGE.nameOfPage
    print(nameOfPage)
    obj = Comment.objects.filter(cat = PAGE)
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())
    return render(request, 'list.html', {'nameOfPage' : nameOfPage, 'idOfPage':idOfPage, 'obj':obj, 'username': username, 'nowTime' : nowTime} )

def newPage(request):
    if request.method == 'POST':
        nameOfPage = request.POST.get('nameOfPage')
    
        return redirect('map:index')
    else:
        pages = MAP.objects.all()
        return redirect('map:index')