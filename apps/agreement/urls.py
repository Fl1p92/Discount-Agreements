from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]

# API endpoint

urlpatterns += format_suffix_patterns([
    path('agreements/calendar/', views.AgreementsCalendarAPIView.as_view(), name='calendar'),
])
