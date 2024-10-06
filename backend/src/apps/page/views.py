
from page.models import Page, Comment
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import  JsonResponse


#функция которая вызывается при переходе на страницу Виртуального мира 
def index(request, idOfPage):
    try:
        page = Page.objects.get(id=idOfPage)
        comments = Comment.objects.filter(ParentPageKey=page)

        # Сериализуем комментарии в список словарей
        comments_data = [
            {
                "commentText": comment.commentText,
                "publishedDate": comment.publishedDate,
                "username": comment.username,
            }
            for comment in comments
        ]

        username = request.session.get('username')
        pageData = [{
            "id": page.id,
            "nameOfPage": page.nameOfPage,
            "username": username,
            "comments": comments_data
        }]

        return JsonResponse({"page": pageData})

    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def leave_comment(request, idOfPage):
    if request.method == 'POST':
        parentPage = get_object_or_404(Page, id=idOfPage)
        username = request.POST.get('username')
        if not username:
            username = 'Anonymous'
        
        commentText = request.POST.get('commentText', '')
      
        if not commentText.strip():
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)

        # Создаем и сохраняем комментарий
        comment = Comment(username=username, commentText=commentText, ParentPageKey=parentPage)
        comment.publishedDate = timezone.now()  # Используем правильное имя поля
        comment.save()

        return JsonResponse({"message": "Comment saved successfully."}, status=201)

    return JsonResponse({"error": "Invalid request method."}, status=405)


    