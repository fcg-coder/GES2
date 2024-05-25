from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'PAGE'

urlpatterns = [
   path('pagelist<int:idOfPage>/', views.index, name='index'),
   path('page<int:idOfPage>/', views.openPage, name='openPage'),
   path('newPAge<int:idOfPage>/', views.newPage, name='newPage'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)