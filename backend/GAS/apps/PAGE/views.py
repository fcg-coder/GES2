from django.shortcuts import render, redirect
from coments.models import Comment
from map.models import MAP
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import page
from map.models import countOfVirW 


def index(request, idOfPage):
    VWS = page.objects.all()
    countOfVirW(VWS)
    category = MAP.objects.get(id = idOfPage)
    print(category.nameOfPage)
    pages = page.objects.filter(map = category)
    nameOfPage = category.nameOfPage


    all_pages = page.objects.all()

    
    
    all_text_tags = set()
    all_graphical_tags = set()

    for page_obj in all_pages:
        all_text_tags.update(page_obj.TEXT_BASED_MMO_CHOICES)
        all_graphical_tags.update(page_obj.GRAPHICAL_MMO_CHOICES)

    print(all_text_tags)
    print(all_graphical_tags)
    
    
    idOfPage = int(idOfPage)
    return render(request, 'listOfPages.html', {'map_internal_pages': pages, 'nameOfPage' : nameOfPage,  'all_text_tags': all_text_tags,
        'all_graphical_tags': all_graphical_tags,} )



def openPage(request, idOfPage):
    print(idOfPage)
    PAGE = page.objects.get(id = idOfPage)
    nameOfPage = PAGE.nameOfPage
    print(nameOfPage)
    obj = Comment.objects.filter(cat = PAGE)
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())
    return render(request, 'list.html', {'nameOfPage' : nameOfPage, 'idOfPage':idOfPage, 'obj':obj, 'username': username, 'nowTime' : nowTime} )



def newPage(request, idOfPage):
    if request.method == 'POST':
        category = request.POST.get('idOfPage')
        text_tags = request.POST.get('all_text_tags')
        graphical_tags = request.POST.get('all_graphical_tags')

        print(text_tags)
        print(graphical_tags)
        map = MAP.objects.get(id=int(category))

        
        nameOfPage = request.POST.get('nameOfPage')
        
        id_arrayM = MAP.objects.values_list('id', flat=True)
        id_arrayP = page.objects.values_list('id', flat=True)
        id_array = list(id_arrayM) + list(id_arrayP)
        id_list = list(id_array)
        newId = max(id_list) + 1 if id_list else 1
        PAGE = page(nameOfPage=nameOfPage, map=map, status= 'pending', id=newId, graphical_MMOs_TAG=graphical_tags, text_based_MMOs_T=text_tags)
        PAGE.save()
        return redirect('map:index')
    else:
        return redirect('map:index')
