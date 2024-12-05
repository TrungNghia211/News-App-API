from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar/%Y/%m', default=None)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description provided")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description provided")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"

class Article(models.Model):
    title = models.CharField(max_length=255, null=False)
    image_url = models.URLField(max_length=200, blank=True, null=True)  
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)  
    content = models.TextField()
    author = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def clean(self):
      
        if self.image_url and self.image_file:
            raise ValidationError("Chỉ được chọn một trong hai: image_url hoặc image_file.")
        if not self.image_url and not self.image_file:
            raise ValidationError("Cần phải chọn ít nhất một trong hai: image_url hoặc image_file.")

class Comment(models.Model):
    title = models.TextField(default="No title") 
    author = models.CharField(max_length=255, null=True, blank=True)  
    created_date = models.DateTimeField(auto_now_add=True)  
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)  

    def __str__(self):
        return self.article[:50]  
