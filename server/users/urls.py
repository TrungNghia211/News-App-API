from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.category_view, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('subcategories/', views.subcategory_view, name='subcategory-list'),
    path('subcategories/<int:pk>/', views.subcategory_detail, name='subcategory-detail'),
    path('subcategories/category/<int:category_id>/', views.subcategories_by_category, name='subcategories_by_category'),
    path('articles/<int:pk>/', views.article_detail, name='articles-detail'),  
    path('articles/', views.article_create_by_subcategory, name='articles-create-by-subcategory'),  
    path('articles/all/', views.article_get_all, name='articles_get_all'),
    path('comments/articles/<int:articles_id>/', views.comment_view, name='add_comment'),
    path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),
]