from django.urls import path

from . import views
from .views import upload_file

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", upload_file, name="upload_file"),
    path('result/', views.result_page, name='result_page'),
]
