from django.urls import path,re_path
from . import views


urlpatterns=[
    path('',views.users_login),
    re_path(r'^mode_select/',views.mode_select),
    re_path(r'^r_mode_select/',views.r_mode_select),
    re_path(r'^deposit/',views.deposit),
    re_path(r'^takeout/',views.takeout),
    re_path(r'^inquire/',views.inquire),
    path('administration/',views.administration),
    re_path(r'^administration/del_user',views.del_user),
    re_path(r'^administration/del_component',views.del_component),
]