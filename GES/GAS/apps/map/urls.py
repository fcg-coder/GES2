from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'map'

urlpatterns = [
    path('', views.index , name='index'),
<<<<<<< HEAD
    path('next_page/<int:idToNewPage>/<str:nameOfPage>/', views.next_page, name='next_page'),
    path('newPage/', views.newPage, name='newPage'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('<int:idToNewPage>/', views.next_page, name='next_page'),
    path('graph/', views.graph, name='graph'),
    path('diagram/', views.euler_diagram_view, name='euler_diagram_view'),
    path('createNewPage/', views.createNewPage, name='createNewPage'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> master
