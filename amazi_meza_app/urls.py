from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^home$', views.home, name='home'),
    url(r'^problems$', views.problems, name='problems'),
    url(r'^mapping$', views.mapping, name='mapping'),
    url(r'^finance$', views.finance, name='finance'),
]