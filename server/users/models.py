from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar/%Y/%m', default=None)
    phone = models.CharField(max_length=15, blank=True, null=True)  
    birthday = models.DateField(null=True, blank=True)  
    address = models.CharField(max_length=255, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.username
    
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
    title = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200, blank=True, null=True)  
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)  
    content = models.TextField()
    author = models.CharField(max_length=255, default="Unknown Author") 
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def clean(self):
        if self.image_url and self.image_file:
            raise ValidationError("Chỉ được chọn một trong hai: image_url hoặc image_file.")
        if not self.image_url and not self.image_file:
            raise ValidationError("Cần phải chọn ít nhất một trong hai: image_url hoặc image_file.")


class Comment(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.article.title if self.article else 'No Article'})"

class SoftDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
