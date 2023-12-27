from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'map'

urlpatterns = [
    path('', views.index , name='index'),
    path('next_page/<int:idToNewPage>/<str:nameOfPage>/', views.next_page, name='next_page'),
    path('newPage/<int:idOfPage>/', views.newPage, name='newPage'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)