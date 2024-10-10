from django.http import  JsonResponse
from category.models import Category
from django.views.decorators.csrf import csrf_exempt


# Возвращает данные о категориях (Переход между ними)
# Пропсать логику для конечной категории 
#  if flagForIncludedCategorys == 0 :
#  Вернуть список СТРАНИЦ Page модели 


def index(reuest):
    try:
        categories = Category.objects.filter(flagForThePresenceOfAParent=0)
        
        # Если нет нужных категорий, возвращаем пустой JSON
        if not categories.exists():
            return JsonResponse({"categories": []})
        
        # Находим относительный размер категории для хорошего отображения
        allSize = sum(category.countOfNestedWorld for category in categories)

        for category in categories:
            category.size = category.countOfNestedWorld / allSize if allSize > 0 else 0  # Проверка на деление на ноль
            category.save()

        # Собираем все в JSON и возвращаем во фронт
        categoriesData = [{"id": category.id, "nameOfCatergory": category.nameOfCatergory, "size": category.size} for category in categories]  # Исправлено: `catergory` на `category`
        return JsonResponse({"categories": categoriesData})

    except Exception as e:
        print("Error:", str(e))  # Вывод ошибки
        return JsonResponse({"error": str(e)}, status=500)

