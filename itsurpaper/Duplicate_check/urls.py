from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("submit", views.submit, name="submit_page"),
    path('result/', views.result_page, name='result_page'),
]
