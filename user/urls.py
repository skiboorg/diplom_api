from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('my_users', views.GetMyUsers.as_view()),
    path('add_user', views.AddUser.as_view()),
    path('update_user', views.UpdateUser.as_view()),
    path('get_networks', views.GetNetworks.as_view()),
    path('get_user/<uuid>', views.GetUserByUuid.as_view()),
    path('delete_user/<uuid>', views.DeleteUser.as_view()),
    path('delete_user_file/<id>', views.DeleteUserFile.as_view()),
    path('delete_user_comment/<id>', views.DeleteUserComment.as_view()),
    path('add_user_comment/<uuid>', views.AddUserComment.as_view()),
    path('delete_user_network/<id>', views.DeleteUserNetwork.as_view()),









]
