from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('com', views.communicate, name='communicate')
]