
# Импорт функции для перенаправления и рендеринга шаблонов в Django
from django.shortcuts import redirect, render

# Импорт класса для отправки email-сообщений
from django.core.mail import EmailMessage

# Импорт класса для перенаправления HTTP ответов
from django.http import HttpResponseRedirect

# Импорт модели feedback из текущего приложения
from .models import Feedback

# Импорт модели Category из приложения category
from category.models import Category

# Импорт библиотеки Plotly для работы с графиками
import plotly.graph_objects as go
# Импорт библиотеки networkx для работы с графами


# Импорт всех зарегистрированных приложений в проекте
from django.apps import apps

# Импорт библиотеки для работы с бинарными данными
import pickle
from django.http import JsonResponse

# Импорт JSON сериализатора из Django

# Повторный импорт модели Category из приложения category (здесь это избыточно)
from category.models import Category

# Импорт модели page из приложения page
from page.models import Page

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
        fb = Feedback(name=name, email=email, subject=subject, message=message, attachment=attachment)
        fb.save()
        
        # Перенаправляем пользователя после успешной отправки формы
        return redirect('category:index')

    # Если запрос не POST, перенаправляем пользователя на главную страницу
    return redirect('category:index')


# Функция для создания новой страницы (возможно, стоит вынести в сервис)
def createNewPage(request):
    # Получаем категории из модели Category, у которых FlagForInternalRecordings равно 0
    category = Category.objects.filter(FlagForInternalRecordings=0).values('id', 'nameOfPage')
    
    # Получаем все страницы из модели page
    all_pages = Page.objects.all()

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


# Функция для отображения диаграммы Эйлера-Венна
def euler_diagram_view(request):
    # Получаем данные из моделей Category и page
    category_data = Category.objects.all()
    page_data = Page.objects.all()

    # Создаем списки меток и родительских меток для модели Category
    category_labels = [entry.nameOfPage for entry in category_data]
    category_parents = ['' if entry.FlagForThePresenceOfAParent == 0 else Category.objects.get(internal_pages=entry).nameOfPage for entry in category_data]

    # Создаем списки меток и родительских меток для модели page
    page_labels = [entry.nameOfPage for entry in page_data]
    page_parents = [entry.category.nameOfPage for entry in page_data]

    # Объединяем списки меток и родительских меток из двух моделей
    labels = category_labels + page_labels
    parents = category_parents + page_parents

    # Устанавливаем первых двух родителей как 'ALL'
    parents[0] = 'ALL'
    parents[1] = 'ALL'

    # Значения для каждого узла, важен только их относительный размер
    values = [1 for _ in labels]

    # Создаем диаграмму Эйлера-Венна с помощью Plotly Treecategory
    fig = go.Figure(go.Treecategory(
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
    fig.write_html('src/templates/euler_diagram.html')

    # Отображаем сгенерированную диаграмму на странице
    return render(request, 'euler_diagram.html')
