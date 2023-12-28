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
    map_obj = MAP.objects.get(id = idToNewPage)
    FlagForInternalRecordingsPAGE = map_obj.FlagForInternalRecordings

    FlagForThePresenceOfAParentPAGE = map_obj.FlagForThePresenceOfAParent
    nameOfPage = nameOfPage
    newPage = MAP(id=id, nameOfPage = nameOfPage, status = 'published', FlagForThePresenceOfAParent = FlagForThePresenceOfAParentPAGE, FlagForInternalRecordings = FlagForInternalRecordingsPAGE)
    newPage.save()
    return redirect('comments:index', idOfPage=id)


#ДОБАВИТЬ КАВЕР 
def newPage(request, idOfPage):
    if request.method == 'POST':
        map_instance = MAP.objects.get(id=idOfPage)
        map_instance.FlagForInternalRecordings = 1
        map_instance.save()
        nameOfPage = request.POST.get('nameOfPage')
        pages = MAP.objects.all()
        max_index = max(pages, key=lambda x: x.id) 
        page = MAP(nameOfPage=nameOfPage, id=max_index.id+1, status = 'pending', FlagForThePresenceOfAParent=1)
        page.save()
        pages = MAP.objects.all()
        map_instance.internal_pages.add(page.id)
        return redirect('map:index')
    else:
        pages = MAP.objects.all()
        return redirect('map:index')
    
def graph(request):
    G = nx.Graph()
    instances = MAP.objects.all()

    # Добавление узлов и связей в граф
    for instance in instances:
        G.add_node(instance.id, name=instance.nameOfPage)  # Добавляем узел с атрибутом name
        for related_instance in instance.internal_pages.all():
            G.add_node(related_instance.id, name=related_instance.nameOfPage)  # Добавляем связанный узел
            G.add_edge(instance.id, related_instance.id)

    print(G)
    return render(request, 'graph.html', {'G': G })






