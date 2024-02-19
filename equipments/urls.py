from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.data, name="data"),
    path("<int:equipment_id>", views.detail, name="detail"),
    path("qrcodeid/", views.qrcodeid, name="qrcodeid"),
    path("qrcode_detail/", views.qrcode_detail, name="qrcode_detail"),
    path("get_client_location/", views.get_client_location, name="get_client_location"),

]