from django.urls import path
from . import views

app_name = 'userauths'

urlpatterns = [
    path('signup/', views.signup, name='signup'),

]
