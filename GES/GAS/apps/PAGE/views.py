from django.shortcuts import render, redirect
from coments.models import Comment
from map.models import MAP
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def index(request, idOfPage):
    idOfPage = int(idOfPage)
    print(idOfPage)
    map_instance = MAP.objects.get(id=idOfPage)  # Используйте 'id' вместо 'idOfPage'
    nameOfPage = map_instance.nameOfPage
    map_internal_pages = map_instance.internal_pages.all()
   
    idOfPage = int(idOfPage)
    obj = Comment.objects.all()
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())
    return render(request, 'list.html', {'obj': obj, 'idOfPage': idOfPage, 'username': username, 'nowTime' : nowTime, 'nameOfPage' : nameOfPage,  'map_internal_pages' : map_internal_pages} )
