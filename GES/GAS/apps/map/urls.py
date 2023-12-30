from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'map'

urlpatterns = [
    path('', views.index , name='index'),
    path('<int:idToNewPage>/', views.next_page, name='next_page'),
    path('newPage/<int:idOfPage>/', views.newPage, name='newPage'),
    path('graph/', views.graph, name='graph'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)