from django.shortcuts import render, redirect
from .models import Comment
from map.models import MAP
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import FileCommentForm

def index(request, idOfPage):
    idOfPage = int(idOfPage)
    obj = Comment.objects.all()
    return render(request, 'comments/list.html', {'obj': obj, 'idOfPage': idOfPage} )

@csrf_exempt
def leave_comment(request, idOfPage):
    if request.method == 'POST':
        Pageid = int(idOfPage)
        print(Pageid)
        comment_text = request.POST.get('comment_text', '')  # Второй аргумент - пустая строка, которая будет использоваться по умолчанию, если ключ отсутствует
        document = request.FILES.get('document')
        if document != None:
            documentName = document.name
        else:
            documentName = ''
        comment = Comment(comment_text=comment_text, document=document,
        documentName = documentName, idOfPage = Pageid)
        comment.pub_date = timezone.now()  # добавляем значение для поля pub_date
        comment.save()
        return redirect('comments:index', idOfPage=Pageid) # Если ни комментария, ни файла нет, возвращаем ошибку или делаем что-то другое по вашему усмотрению
    else:
        form = FileCommentForm()
        return render(request, 'comment_form.html', {'form': form})
    