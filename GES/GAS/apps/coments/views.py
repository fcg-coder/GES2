from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from .models import Comment
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .forms import FileCommentForm

def index(request):
    obj = Comment.objects.all()
    return render(request, 'comments/list.html', {'obj': obj})

@csrf_exempt
def leave_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '')  # Второй аргумент - пустая строка, которая будет использоваться по умолчанию, если ключ отсутствует
        document = request.FILES.get('document')
        photo = request.FILES.get('photo')
        if document != None:
            documentName = document.name
        else:
            documentName = ''
        if photo != None:
            photoName = photo.name
        else:
            photoName = ''
        comment = Comment(comment_text=comment_text, document=document,
        documentName = documentName, photo = photo)
        comment.pub_date = timezone.now()  # добавляем значение для поля pub_date
        comment.save()
        return redirect('comments:index') # Если ни комментария, ни файла нет, возвращаем ошибку или делаем что-то другое по вашему усмотрению
    else:
        form = FileCommentForm()
        return render(request, 'comment_form.html', {'form': form})
    
    return redirect('comments:index') # Если ни комментария, ни файла нет, возвращаем ошибку или делаем что-то другое по вашему усмотрению
        