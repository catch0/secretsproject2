from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout', views.logout),
    url(r'^spill',views.spill),
    url(r'^juice', views.juice),
    url(r'^delete/(?P<find>\d*)',views.delete, name='delete'),
    url(r'^like/(?P<find>\d*)',views.like, name='like'),
    url(r'popular', views.popular),
    url(r'back' ,views.back),
]