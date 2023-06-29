from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    


class Post(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author,on_delete= models.SET_NULL, null=True, related_name="posts")
    date = models.DateField(auto_now=True)
    content = RichTextUploadingField()
    slug = models.SlugField(db_index=True, unique=True)
    preview_image = models.ImageField(upload_to="preview_images", null=True)