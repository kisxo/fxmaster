from django.urls import path
from . import views

app_name = "fxsimulator"
urlpatterns = [
    path("", views.index, name="index"),
    path("fx/", views.fxtrade, name="fxtrade"),
    path("accounts/profile/", views.profile, name="profile"),
    
   # path("pick/<int:side>/<int:amount>", views.pick, name="pick"),
]
