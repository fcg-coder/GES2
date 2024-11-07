from django.http import  JsonResponse
from category.models import Category
from page.models import Page
from django.views.decorators.csrf import csrf_exempt
import networkx as nx
from django.core.serializers.json import DjangoJSONEncoder

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
        categoriesData = [{"id": category.id, "nameOfCategory": category.nameOfCategory, "size": category.size} for category in categories]  # Исправлено: `catergory` на `category`
        return JsonResponse({"categories": categoriesData})

    except Exception as e:
        print("Error:", str(e))  # Вывод ошибки
        return JsonResponse({"error": str(e)}, status=500)


def get_category_data(request, category_id):
    try:
        # Получаем категорию по ID
        category = Category.objects.get(id=category_id)

        # Проверяем флаг для наличия внутренних записей (flagForInternalRecordings)
        category_data = {
            "id": category.id,
            "nameOfCategory": category.nameOfCategory,
            "flagForInternalRecordings": category.flagForInternalRecordings,  # Добавлен флаг
            "flagForThePresenceOfAParent": category.flagForThePresenceOfAParent  # Добавлен флаг
        }

        # Если флаг для внутренних записей равен True, то категория конечная
        if category.flagForInternalRecordings == False:
            # Если категория конечная, возвращаем страницы из модели Page
            pages = Page.objects.filter(parentCategoryKey=category)
            pages_data = [{"id": page.id, "nameOfPage": page.nameOfPage} for page in pages]
            
            return JsonResponse({
                "category": category_data,  # Возвращаем категорию с флагами
                "pages": pages_data
            })

        else:
            # Если категория не конечная, возвращаем подкатегории
            subcategories = category.childCategoies.all()
            subcategories_data = []
            
            # Проходим по всем подкатегориям и добавляем флаги
            for subcategory in subcategories:
                subcategory_data = {
                    "id": subcategory.id,
                    "nameOfCategory": subcategory.nameOfCategory,
                    "flagForInternalRecordings": subcategory.flagForInternalRecordings,  # Флаг подкатегории
                    "flagForThePresenceOfAParent": subcategory.flagForThePresenceOfAParent  # Флаг подкатегории
                }
                subcategories_data.append(subcategory_data)

            return JsonResponse({
                "category": category_data,  # Возвращаем категорию с флагами
                "subcategories": subcategories_data  # Возвращаем подкатегории с флагами
            })

    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)
    except Exception as e:
        print("Error:", str(e))  # Вывод ошибки
        return JsonResponse({"error": str(e)}, status=500)


# Функция для генерации графа и его отправки на фронтенд
def graph(request):
    # Создаем пустой граф с помощью networkx
    G = nx.Graph()
    
    # Получаем все категории из модели Category
    categories = Category.objects.all()
    
    # Добавляем узлы и связи в граф для каждой категории
    for category in categories:
        G.add_node(category.id, name=category.nameOfCategory)
        
        # Если категория имеет внутренние записи, добавляем их как узлы и связываем с родительской категорией
        if category.flagForInternalRecordings:
            for subcategory in category.childCategoies.all():
                G.add_node(subcategory.id, name=subcategory.nameOfCategory)
                G.add_edge(category.id, subcategory.id)
        
        # Если категория не имеет внутренних записей, связываем ее с объектами из модели Page
        else:
            pages = Page.objects.filter(parentCategoryKey=category)
            for page in pages:
                # Добавляем префикс к идентификатору страницы, чтобы избежать конфликта
                page_id = f'page_{page.id}'
                G.add_node(page_id, name=page.nameOfPage)
                G.add_edge(category.id, page_id)
    
    # Подготавливаем данные для отправки на фронтенд в формате JSON
    nodes = [{'id': node, 'label': data['name']} for node, data in G.nodes(data=True)]
    edges = [{'from': u, 'to': v} for u, v in G.edges()]
    
    # Отправляем данные как JSON-ответ
    return JsonResponse({'nodes': nodes, 'edges': edges}, encoder=DjangoJSONEncoder)
