from django.shortcuts import render, redirect
from .models import Comment
from PAGE.models import page
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import FileCommentForm

def index(request, idOfPage):
    idOfPage = int(idOfPage)
    map_instance = page.objects.get(id=idOfPage)  # Используйте 'id' вместо 'idOfPage'
    nameOfPage = map_instance.nameOfPage
    map_internal_pages = map_instance.internal_pages.all()
   
    idOfPage = int(idOfPage)
    obj = Comment.objects.all()
    username = request.session.get('username')
    nowTime = timezone.localtime(timezone.now(), timezone.get_current_timezone())
    return render(request, '', {'obj': obj, 'idOfPage': idOfPage, 'username': username, 'nowTime' : nowTime, 'nameOfPage' : nameOfPage,  'map_internal_pages' : map_internal_pages} )

@csrf_exempt
def leave_comment(request, idOfPage):
    if request.method == 'POST':
        Pageid = int(idOfPage)
        Page = page.objects.get(id = idOfPage)
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
                return redirect('PAGE:openPage', idOfPage=Pageid)
            else:
                documentName = document.name
                adminNameComment = document.name

        else:
            adminNameComment = comment_text
        
       
        comment = Comment(username = username, comment_text=comment_text, document=document,
        documentName = documentName, adminNameComment = adminNameComment, cat = Page)
        comment.pub_date = timezone.now()  # добавляем значение для поля pub_date
        comment.save()
        return redirect('PAGE:openPage', idOfPage=Pageid) # Если ни комментария, ни файла нет, возвращаем ошибку или делаем что-то другое по вашему усмотрению
    else:
        form = FileCommentForm()
        return render(request, 'comment_form.html', {'form': form})
    