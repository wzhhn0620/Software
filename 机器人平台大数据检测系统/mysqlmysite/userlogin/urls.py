from django.urls import path,re_path
from . import views


urlpatterns=[
    path('',views.user_login),
    re_path(r'^class/',views.class_show),
    re_path(r'^data_show/',views.data_show),
    re_path(r'^add_class/',views.add_class),
    re_path(r'^download_class/',views.download_class),
    re_path(r'^edit_class/',views.edit_class),
    re_path(r'^edit_data/',views.edit_data),
]