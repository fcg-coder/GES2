from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'service'

urlpatterns = [
   path('feedback_submit/', views.feedback_submit, name='feedback_submit'),
   path('graph/', views.graph, name='graph'),
   path('diagram/', views.euler_diagram_view, name='euler_diagram_view'),
   path('createNewPage/', views.createNewPage, name='createNewPage'),

  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)