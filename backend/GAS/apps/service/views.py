from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from .models import feedback
from map.models import MAP

def feedback_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')  # Получаем прикрепленный файл, если он есть
        

         # Создаем объект EmailMessage
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=email,
            to=['stasyanrus610@gmail.com'],
        )
        
        # Прикрепляем файл, если он есть
        if attachment:
            email_message.attach(attachment.name, attachment.read(), attachment.content_type)
        
        # Отправка сообщения
        #email_message.send()

        fb = feedback(name = name, email = email,subject = subject, message = message,  attachment = attachment)
        fb.save()
        # Перенаправление пользователя после отправки формы
        return redirect('map:index')

    return redirect('map:index')
