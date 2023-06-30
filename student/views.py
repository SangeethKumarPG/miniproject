from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from .models import Registration

# Create your views here.

class StudentRegistrationView(CreateView):
    form_class = RegistrationForm
    model = Registration
    template_name = "student/student_registration.html"
    success_url = "/"
