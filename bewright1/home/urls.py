from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot),
    path('index', views.index),
    path('vegetables', views.vegetables),
    path('about', views.about),
    path('contact', views.contact),
    path('shop', views.shop),
    path('chatbot', views.chatbot),
    path('get_bot_response/', views.get_bot_response_view, name='get_bot_response'),
]
