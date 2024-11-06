from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'category'

urlpatterns = [
    path('', views.index , name='index'),
    path('<int:category_id>/', views.get_category_data, name='get_category_data'),
    path('graph/', views.graph, name='graph'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
