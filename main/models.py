from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    rasm = models.ImageField(upload_to="photo")
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.name
    
class Kitob(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    rasm = models.ImageField(upload_to="photo")
    file = models.FileField(upload_to="file")
    created = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField()
    info = models.TextField()
    more_info = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
class BookDownloads(models.Model):
    count = models.IntegerField()
    

class Comments(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(to=Kitob, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
class Shortner(models.Model):
    url = models.TextField()
    code = models.CharField(max_length=40)
    
class ResetPassword(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)