

# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView,UpdateView
from .models import Post
from .forms import PostForm

from django.views.generic import TemplateView, ListView
# Create your views here.

class MainView(ListView):
    template_name = "blog/index.html"
    model = Post
    def get_queryset(self):
        data =  super().get_queryset()
        return data.order_by("-date")

class CreatePostView(CreateView):
    form_class = PostForm
    model = Post
    template_name = "blog/new_post.html"
    success_url = "/"

class SinglePost(DetailView):
    model = Post
    template_name = "blog/single_post.html"

class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/edit_post.html"
    success_url = "/"

