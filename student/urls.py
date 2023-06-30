from django.urls import path
from . import views

urlpatterns = [
    path("",views.StudentRegistrationView.as_view(), name="register"),
]
