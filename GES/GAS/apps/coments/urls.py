from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'comments'

urlpatterns = [
    path('<int:idOfPage>/', views.index, name='index'),
    path('leave_comment/<int:idOfPage>/', views.leave_comment, name='leave_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)