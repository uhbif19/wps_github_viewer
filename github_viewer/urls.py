from django.contrib import admin
from django.urls import path, include

from viewer import views


urlpatterns = [
    path('', views.ViewAccount.as_view()),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
]
