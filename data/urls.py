from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('order/statuses', views.OrderStatus.as_view()),
    path('order/pay_statuses', views.PayStatus.as_view()),

    path('orders/by_manager/<created_by__uuid>', views.ManagerOrder.as_view()),
    path('orders/by_user/<user__uuid>', views.UserOrder.as_view()),
    path('order/file/<pk>', views.FileOrder.as_view()),


    path('order/<uuid>/comment/<comment_id>', views.OrderComments.as_view()),
    path('order/<uuid>/file/<file_id>', views.OrderFiles.as_view()),
    path('service_by_country', views.ServiceByCountry.as_view()),
    path('', include(router.urls)),

]
