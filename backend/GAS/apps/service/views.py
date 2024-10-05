
# Импорт функции для перенаправления и рендеринга шаблонов в Django
from django.shortcuts import redirect, render

# Импорт класса для отправки email-сообщений
from django.core.mail import EmailMessage

# Импорт класса для перенаправления HTTP ответов
from django.http import HttpResponseRedirect

# Импорт модели feedback из текущего приложения
from .models import feedback

# Импорт модели MAP из приложения map
from map.models import MAP

# Импорт библиотеки Plotly для работы с графиками
import plotly.graph_objects as go

# Импорт библиотеки networkx для работы с графами
import networkx as nx

# Импорт всех зарегистрированных приложений в проекте
from django.apps import apps

# Импорт библиотеки для работы с бинарными данными
import pickle
from django.http import JsonResponse

# Импорт JSON сериализатора из Django
from django.core.serializers.json import DjangoJSONEncoder

# Повторный импорт модели MAP из приложения map (здесь это избыточно)
from map.models import MAP

# Импорт модели page из приложения PAGE
from PAGE.models import page

# Функция для обработки формы обратной связи
def feedback_submit(request):
    # Проверяем, был ли запрос методом POST
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')  # Получаем прикрепленный файл, если он есть
        
        # Создаем объект EmailMessage для отправки письма
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=email,
            to=['stasyanrus610@gmail.com'],
        )
        
        # Прикрепляем файл к письму, если он был загружен
        if attachment:
            email_message.attach(attachment.name, attachment.read(), attachment.content_type)
        
        # Отправляем письмо (закомментировано)
        # email_message.send()

        # Создаем объект обратной связи и сохраняем его в базе данных
        fb = feedback(name=name, email=email, subject=subject, message=message, attachment=attachment)
        fb.save()
        
        # Перенаправляем пользователя после успешной отправки формы
        return redirect('map:index')

    # Если запрос не POST, перенаправляем пользователя на главную страницу
    return redirect('map:index')


# Функция для создания новой страницы (возможно, стоит вынести в сервис)
def createNewPage(request):
    # Получаем категории из модели MAP, у которых FlagForInternalRecordings равно 0
    category = MAP.objects.filter(FlagForInternalRecordings=0).values('id', 'nameOfPage')
    
    # Получаем все страницы из модели page
    all_pages = page.objects.all()

    # Инициализируем множества для хранения уникальных текстовых и графических тегов
    all_text_tags = set()
    all_graphical_tags = set()

    # Проходим по всем страницам и добавляем их текстовые и графические теги в соответствующие множества
    for page_obj in all_pages:
        all_text_tags.update(page_obj.TEXT_BASED_MMO_CHOICES)
        all_graphical_tags.update(page_obj.GRAPHICAL_MMO_CHOICES)

    # Рендерим страницу с передачей категорий и тегов в контекст
    return render(request, 'createNewPage.html', {
        'category': category,
        'all_text_tags': all_text_tags,
        'all_graphical_tags': all_graphical_tags,
    })


# Функция для генерации графа и его отправки на фронтенд
def graph(request):
    # Создаем пустой граф с помощью networkx
    G = nx.Graph()
    
    # Получаем все категории из модели MAP
    categorys = MAP.objects.all()
    
    # Добавляем узлы и связи в граф для каждой категории
    for category in categorys:
        G.add_node(category.id, name=category.nameOfPage)
        
        # Если категория имеет внутренние записи, добавляем их как узлы и связываем с родительской категорией
        if category.FlagForInternalRecordings == 1:
            for podcategory in category.internal_pages.all():
                G.add_node(podcategory.id, name=podcategory.nameOfPage)
                G.add_edge(category.id, podcategory.id)
        
        # Если категория не имеет внутренних записей, связываем ее с объектами из модели page
        if category.FlagForInternalRecordings == 0:
            objs = page.objects.filter(map=category)
            for obj in objs:
                G.add_node(obj.id, name=obj.nameOfPage)
                G.add_edge(category.id, obj.id)
    
    # Подготавливаем данные для отправки на фронтенд в формате JSON
    nodes = [{'id': node, 'label': data['name']} for node, data in G.nodes(data=True)]
    edges = [{'from': u, 'to': v} for u, v in G.edges()]
    
    # Отправляем данные как JSON-ответ
    return JsonResponse({'nodes': nodes, 'edges': edges}, encoder=DjangoJSONEncoder)


# Функция для отображения диаграммы Эйлера-Венна
def euler_diagram_view(request):
    # Получаем данные из моделей MAP и page
    map_data = MAP.objects.all()
    page_data = page.objects.all()

    # Создаем списки меток и родительских меток для модели MAP
    map_labels = [entry.nameOfPage for entry in map_data]
    map_parents = ['' if entry.FlagForThePresenceOfAParent == 0 else MAP.objects.get(internal_pages=entry).nameOfPage for entry in map_data]

    # Создаем списки меток и родительских меток для модели page
    page_labels = [entry.nameOfPage for entry in page_data]
    page_parents = [entry.map.nameOfPage for entry in page_data]

    # Объединяем списки меток и родительских меток из двух моделей
    labels = map_labels + page_labels
    parents = map_parents + page_parents

    # Устанавливаем первых двух родителей как 'ALL'
    parents[0] = 'ALL'
    parents[1] = 'ALL'

    # Значения для каждого узла, важен только их относительный размер
    values = [1 for _ in labels]

    # Создаем диаграмму Эйлера-Венна с помощью Plotly Treemap
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo='label+value+percent entry',
        hoverinfo='all',
        marker=dict(
            colors=['blue', 'red', 'green', 'yellow']  # Указываем цвета для каждой метки
        )
    ))

    # Настраиваем внешний вид диаграммы
    fig.update_layout(
        title='Диаграмма Эйлера-Венна',
    )

    # Сохраняем диаграмму в виде HTML-файла
    fig.write_html('GAS/templates/euler_diagram.html')

    # Отображаем сгенерированную диаграмму на странице
    return render(request, 'euler_diagram.html')
