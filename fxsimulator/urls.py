from django.urls import path
from . import views

app_name = "fxsimulator"
urlpatterns = [
    path("", views.fxtrade, name="fxtrade"),
    path("order/", views.fxorder, name="fxorder"),
    path("accounts/profile/", views.profile, name="profile"),
]
