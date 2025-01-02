from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/categories/', views.category_view, name='category-list'),
    path('api/categories/<int:pk>/', views.category_detail, name='category-detail'),

    path('api/subcategories/', views.subcategory_view, name='subcategory-list'),
    path('api/subcategories/<int:pk>/', views.subcategory_detail, name='subcategory-detail'),
    path('api/subcategories/category/<int:category_id>/', views.subcategories_by_category, name='subcategories_by_category'),

    path('api/articles/<int:pk>/', views.article_detail, name='articles-detail'),  
    path('api/articles/', views.article_create_by_subcategory, name='articles-create-by-subcategory'),  
    path('api/articles/all/', views.article_get_all, name='articles_get_all'),
    path('api/articles/<int:id>/increase-view/', views.increase_view, name='increase_view'),
    path('api/articles/category/<int:category_id>/', views.articles_by_category, name='articles-by-category'),
    path('api/articles/subcategory/<int:subcategory_id>/', views.articles_by_subcategory, name='articles-by-subcategory'),
    
    path('api/comments/articles/<int:articles_id>/', views.comment_view, name='add_comment'),
    path('api/comments/user/<int:user_id>/', views.comment_view_userID, name='comments_by_user'),
    path('api/comments/<int:pk>/', views.comment_detail, name='comment_detail'),

    path('api/upload/', views.upload_image, name='upload-image'),
    
]