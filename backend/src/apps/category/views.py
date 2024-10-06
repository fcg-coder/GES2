from django.http import  JsonResponse
from category.models import Category
from django.views.decorators.csrf import csrf_exempt


# Возвращает данные о категориях (Переход между ними)
# Пропсать логику для конечной категории 
#  if flagForIncludedCategorys == 0 :
#  Вернуть список СТРАНИЦ Page модели 
def index(request):
    try:
        categories = Category.objects.filter(flagForThePresenceOfAParent=0)

        # Находим относительный размер категории для хорошего отображения
        allSize = sum(category.countOfVW for category in categories)

        for category in categories:
            category.size = category.countOfVW / allSize if allSize > 0 else 0  # Проверка на деление на ноль
            category.save()

        # Собираем все в JSON и возвращаем во фронт
        categoriesData = [{"id": category.id, "nameOfCategory": category.nameOfCategory, "size": category.size} for category in categories]  # Исправлено: `catergory` на `category`
        return JsonResponse({"categories": categoriesData})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

