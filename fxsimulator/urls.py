from django.urls import path, include
from fxsimulator import views
from fxsimulator.views import OrderViewSet, ListStockView
from rest_framework.routers import DefaultRouter


app_name = "fxsimulator"
urlpatterns = [
    path("", views.fxtrade, name="fxtrade"),
    path("order/", views.fxorder, name="fxorder"),
    path("stocks/", ListStockView.as_view()),
    path("accounts/profile/", views.profile, name="profile"),
]
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
urlpatterns += router.urls
