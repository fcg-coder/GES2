from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from requests import post
from map.models import MAP
from PAGE.models import page
from PAGE.models import Comment
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder



from .models import countOfVirW 

def index(request):
    try:
        VWS = page.objects.all()
        countOfVirW(VWS)
        find_parents_and_children()
        pages = MAP.objects.filter(FlagForThePresenceOfAParent=0)

        allSize = sum(Page.countOfVW for Page in pages)

        for Page in pages:
            Page.size = Page.countOfVW / allSize
            Page.save()

        pages_data = [{"id": Page.id, "nameOfPage": Page.nameOfPage, "size": Page.size} for Page in pages]
        return JsonResponse({"pages": pages_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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

    allSize = 0
    for Page in map_internal_pages:
        allSize += Page.countOfVW


    for Page in map_internal_pages:
        Page.size = round(Page.countOfVW/allSize * 10)
        print(Page.size)
        Page.save()


    FlagForInternalRecordingsPAGE = map_obj.FlagForInternalRecordings
    if (map_obj.internal_pages == None):
        FlagForInternalRecordingsPAGE = 0

    FlagForThePresenceOfAParentPAGE = map_obj.FlagForThePresenceOfAParent
    newPage = MAP(id=id, nameOfPage = nameOfPage, FlagForThePresenceOfAParent = FlagForThePresenceOfAParentPAGE, FlagForInternalRecordings = FlagForInternalRecordingsPAGE)
    newPage.save()
    

    data = {
        'idOfPage': int(idToNewPage),
        'nameOfPage': nameOfPage,
        'map_internal_pages': [{
            'id': page.id,
            'countOfVW': page.countOfVW,
            'size': page.size,
            # Добавьте другие поля, которые вам нужны из модели MAPInternalPages
        } for page in map_internal_pages],
        'username': username,
        'nowTime': nowTime.strftime('%Y-%m-%d %H:%M:%S'),  # Форматируем дату и время
    }

    # Возвращаем JsonResponse с подготовленными данными
    return JsonResponse(data)





