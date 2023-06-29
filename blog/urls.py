from django.urls import path
from . import views

urlpatterns = [
    path("",views.MainView.as_view(), name="home"),
    path("newpost/",views.CreatePostView.as_view(), name='new_post'),
    path("post/<int:pk>", views.SinglePost.as_view()),
    path("updatepost/<int:pk>", views.UpdatePostView.as_view(), name="update_post")
]
