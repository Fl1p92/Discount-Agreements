from django.urls import path

from . import views


urlpatterns = [
    path('', views.SendMailView.as_view(), name='send_mail'),
]
