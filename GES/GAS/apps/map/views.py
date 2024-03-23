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

from .models import countOfVirW 

def index(request):
    id = int(0)
    VWS = page.objects.all()
    countOfVirW(VWS)
    find_parents_and_children()
    pages = MAP.objects.filter(FlagForThePresenceOfAParent=0)
   
    
 
    return render(request, 'base.html', {'pages': pages})


def find_parents_and_children():
    all_maps = MAP.objects.all()

    # Проходимся по каждому объекту
    for map_obj in all_maps:
        # Получаем дочерние страницы текущего объекта
        child_pages = map_obj.internal_pages.all()
        
        # Если у текущего объекта есть дочерние страницы
        if child_pages.exists():
            # Проходимся по каждой дочерней странице
            for child_page in child_pages:
                # Устанавливаем для дочерней страницы родительскую страницу текущего объекта
                child_page.parent_page = map_obj
                child_page.save()

    # Проходимся по каждому объекту снова
    for map_obj in all_maps:
        # Получаем родительскую страницу текущего объекта
        parent_page = map_obj.parent_page

        # Если у текущего объекта есть родительская страница
        if parent_page:
            # Получаем все дочерние страницы для родительской страницы
            child_pages = parent_page.internal_pages.all()

            # Если дочерние страницы существуют
            if child_pages.exists():
                # Проверяем, что текущий объект находится среди дочерних страниц
                if map_obj in child_pages:
                    # Выводим родительскую страницу и ее дочерние страницы
                    print(f"Родительская страница: {parent_page}")
                    print("Дочерние страницы:")
                    for child_page in child_pages:
                        print(child_page)
                        
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

def createNewPage(request):
    category =  MAP.objects.filter(FlagForInternalRecordings=0).values('id', 'nameOfPage')
    all_pages = page.objects.all()

    
    
    all_text_tags = set()
    all_graphical_tags = set()

    for page_obj in all_pages:
        all_text_tags.update(page_obj.TEXT_BASED_MMO_CHOICES)
        all_graphical_tags.update(page_obj.GRAPHICAL_MMO_CHOICES)

    return render(request, 'createNewPage.html',{'category' : category  , 'all_text_tags': all_text_tags,
        'all_graphical_tags': all_graphical_tags,} )


    



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