from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create_equipment", views.create_equipment, name="create_equipment"),
    path("<int:equipment_id>", views.detail, name="detail"),
]