from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.new),
    url(r'^create_user$', views.create_user),
    url(r'^edit$', views.edit),
    url(r'^edit_info/(?P<number>\d+)$', views.edit_info),
    url(r'^edit_pw/(?P<number>\d+)$', views.edit_pw),
    url(r'^edit_desc/(?P<number>\d+)$', views.edit_desc),
    url(r'^edit_user/(?P<number>\d+)$', views.edit_user),
    url(r'^delete_user/(?P<number>\d+)$', views.delete_user),
    url(r'^make_admin/(?P<number>\d+)$', views.make_admin),
    url(r'^remove_admin/(?P<number>\d+)$', views.remove_admin),
    url(r'^show/(?P<number>\d+)$', views.show_user),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^delete_message/(?P<number>\d+)$', views.delete_message),
    url(r'^delete_comment/(?P<number>\d+)$', views.delete_comment)   

]