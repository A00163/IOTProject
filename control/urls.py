from django.urls import path
from . import views


urlpatterns = [
    path('led/', views.control_esp32, name='control_esp32'),
    path('toggle-led/', views.toggle_led, name='toggle_led'),

]