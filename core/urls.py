from django.urls import path
from . import views

urlpatterns = [
    path("fila/", views.fila_view, name="fila"),
    path("controlo/", views.controlo_view, name="controlo"),
]