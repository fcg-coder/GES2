from django.shortcuts import render, redirect
from .models import Comment
from map.models import MAP
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import FileCommentForm

def index(request, idOfPage):
    idOfPage = int(idOfPage)
    map_instance = MAP.objects.get(id=idOfPage)  # Используйте 'id' вместо 'idOfPage'
    nameOfPage = map_instance.nameOfPage
    print(nameOfPage, 'имя страницы')
    idOfPage = int(idOfPage)
    obj = Comment.objects.all()
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())
    return render(request, 'comments/list.html', {'obj': obj, 'idOfPage': idOfPage, 'username': username, 'nowTime' : nowTime, 'nameOfPage' : nameOfPage} )

@csrf_exempt
def leave_comment(request, idOfPage):
    if request.method == 'POST':
        Pageid = int(idOfPage)
        print(Pageid)
        request.session['username'] = request.POST.get('username')
        username = request.session.get('username')
        if username is None:
            username = request.POST.get('username')
            if username is None or username == '':
                username = 'Anonymous'
        comment_text = request.POST.get('comment_text', '')  # Второй аргумент - пустая строка, которая будет использоваться по умолчанию, если ключ отсутствует
        document = request.FILES.get('document')

        documentName = ''
        if comment_text == '':
            if document == None:
                documentName = ''
                return redirect('comments:index', idOfPage=Pageid)
            else:
                documentName = document.name
                adminNameComment = document.name

        else:
            adminNameComment = comment_text
        
       
        comment = Comment(username = username, comment_text=comment_text, document=document,
        documentName = documentName, idOfPage = Pageid, adminNameComment = adminNameComment)
        comment.pub_date = timezone.now()  # добавляем значение для поля pub_date
        comment.save()
        return redirect('comments:index', idOfPage=Pageid) # Если ни комментария, ни файла нет, возвращаем ошибку или делаем что-то другое по вашему усмотрению
    else:
        form = FileCommentForm()
        return render(request, 'comment_form.html', {'form': form})
    