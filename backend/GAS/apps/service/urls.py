from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'service'

urlpatterns = [
   path('feedback_submit/', views.feedback_submit, name='feedback_submit'),
  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)