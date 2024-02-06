from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.data, name="data"),
    path("<int:equipment_id>", views.detail, name="detail"),
    path("graph/", views.generate_graph, name="generate_graph"),

]