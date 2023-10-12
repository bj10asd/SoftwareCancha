from django.urls import path
from reservas import views


urlpatterns = [

    path('',views.index,name='index'),

]

