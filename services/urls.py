from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from services import views

urlpatterns = [
    path('prediction/', csrf_exempt(views.prediction)),
    path('register/', csrf_exempt(views.register))
]