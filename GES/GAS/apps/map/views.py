from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from requests import post
from map.models import MAP
from PAGE.models import page
from coments.models import Comment
import plotly.graph_objects as go
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt


import networkx as nx
from django.apps import apps
import pickle

def index(request):
    id = int(0)
    pages = MAP.objects.all()
    #for page in pages:
     #   print(page.id)
    return render(request, 'base.html',{'pages': pages } )

@csrf_exempt
def next_page(request, idToNewPage):
    


    map_instance = MAP.objects.get(id=idToNewPage)  # Используйте 'id' вместо 'idOfPage'
    nameOfPage = map_instance.nameOfPage
    map_internal_pages = map_instance.internal_pages.all()
   
    idOfPage = int(idToNewPage)
    obj = Comment.objects.all()
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())

    id = int(idToNewPage)
    map_obj = MAP.objects.get(id = idToNewPage)

    FlagForInternalRecordingsPAGE = map_obj.FlagForInternalRecordings
    if (map_obj.internal_pages == None):
        FlagForInternalRecordingsPAGE = 0

    FlagForThePresenceOfAParentPAGE = map_obj.FlagForThePresenceOfAParent
    newPage = MAP(id=id, nameOfPage = nameOfPage, FlagForThePresenceOfAParent = FlagForThePresenceOfAParentPAGE, FlagForInternalRecordings = FlagForInternalRecordingsPAGE)
    newPage.save()
    
    if (FlagForInternalRecordingsPAGE == 1):
        return render(request, 'MAP.html', {'obj': obj, 'idOfPage': idOfPage, 'username': username, 'nowTime' : nowTime, 'nameOfPage' : nameOfPage,  'map_internal_pages' : map_internal_pages} )
    else:
        print(idOfPage)
        return redirect('PAGE:index', idOfPage=idOfPage)


    
def graph(request):
    G = nx.Graph()
    categorys = MAP.objects.all()
    # Добавление узлов и связей в граф
    for category in categorys:
        G.add_node(category.id, name=category.nameOfPage)  # Добавляем узел с атрибутом name
        
        if category.FlagForInternalRecordings == 1:
            for podcategory in category.internal_pages.all():

                G.add_node(podcategory.id, name=podcategory.nameOfPage)  # Добавляем связанный узел
                G.add_edge(category.id, podcategory.id)
            
        if category.FlagForInternalRecordings == 0:
            objs = page.objects.filter(map = category)
            for obj in objs:
                G.add_node(obj.id, name=obj.nameOfPage)  # Добавляем связанный узел
                G.add_edge(category.id, obj.id)
            
    return render(request, 'graph.html', {'G': G })
 

def euler_diagram_view(request):
    # Получите данные из моделей MAP и Page и обработайте их
    map_data = MAP.objects.all()
    page_data = page.objects.all()

    # Создайте список меток и соответствующих родительских меток для модели MAP
    map_labels = [entry.nameOfPage for entry in map_data]
    map_parents = ['' if entry.FlagForThePresenceOfAParent == 0 else MAP.objects.get(internal_pages=entry).nameOfPage for entry in map_data]

    # Создайте список меток и соответствующих родительских меток для модели Page
    page_labels = [entry.nameOfPage for entry in page_data]
    page_parents = [entry.map.nameOfPage for entry in page_data]

    # Объедините списки меток и родительских меток
    labels = map_labels + page_labels
    parents = map_parents + page_parents

    parents[0] = 'ALL'
    parents[1] = 'ALL'



    values = [1 for _ in labels]  # Значения могут быть любыми, важен только их относительный размер

    # Создайте диаграмму Эйлера-Венна с помощью Plotly Treemap
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo='label+value+percent entry',
        hoverinfo='all',
        marker=dict(
            colors=['blue', 'red', 'green', 'yellow']  # Укажите цвета для каждой метки
        )
    ))

    # Настройте внешний вид диаграммы
    fig.update_layout(
        title='Диаграмма Эйлера-Венна',
    )

    # Сохраните диаграмму в виде HTML-файла или отобразите ее на странице
    fig.write_html('GAS/templates/euler_diagram.html')

    # Верните сгенерированную диаграмму в виде ответа от представления
    return render(request, 'euler_diagram.html')