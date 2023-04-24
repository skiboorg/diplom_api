from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('orders/by_manager/<created_by__uuid>', views.ManagerOrder.as_view()),
    path('orders/by_user/<user__uuid>', views.UserOrder.as_view()),
    path('order/file/<pk>', views.FileOrder.as_view()),
    path('order/statuses', views.OrderStatus.as_view()),
    path('order/pay_statuses', views.PayStatus.as_view()),

]
