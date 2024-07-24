from django.urls import path
from . import views

app_name = "fxsimulator"
urlpatterns = [
    path("", views.index, name="index"),
   # path("pick/<int:side>/<int:amount>", views.pick, name="pick"),
]
