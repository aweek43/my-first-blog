from django.conf.urls import urls
from . import views

urlpatterns = [
url(r'^$', views.post_list, name='post_list'),
]
