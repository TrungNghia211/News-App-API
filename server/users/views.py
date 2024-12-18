from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status, serializers
from .models import User, Category, SubCategory, Article, Comment
from .serializers import UserSerializer, CategorySerializer, SubCategorySerializer, ArticleSerializer, CommentSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

category_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Category description', nullable=True),
    },
    required=['name'],  
)

category_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated category name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated category description', nullable=True),
    },
    required=['name'],  
)

subcategory_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='SubCategory name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='SubCategory description', nullable=True),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
    },
    required=['sub', 'category'],  
)

subcategory_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Updated SubCategory name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated SubCategory description', nullable=True),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Category ID'),
    },
    required=['sub', 'category'],  
)
article_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Content title'),
        'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='Content image URL'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content body'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Author name', nullable=True),
        'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is content active?'),
        'subcategory_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='SubCategory ID'),
        'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID', nullable=True),
    },
    required=['title', 'content', 'subcategory_id'],
)

article_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Content title'),
        'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Content image URL'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Content body'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Author name', nullable=True),
        'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is content active?'),
        'subcategory_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated SubCategory ID'),
        'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Category ID', nullable=True),
    },
    required=['title', 'content', 'subcategory_id'],
)

comment_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Author'),
        'article': openapi.Schema(type=openapi.TYPE_INTEGER, description='Article ID'),
    },
    required=['title','author', 'article'],  
)
comment_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Title'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Author'),
        'article': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Article ID'),
    },
    required=['title','author', 'article'],  
)
@swagger_auto_schema(
    method='post',
    request_body=category_request_body,
    responses={201: CategorySerializer, 400: "Invalid input"}
)
@swagger_auto_schema(
    method='get',
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET', 'POST'])
def category_view(request):
    
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: CategorySerializer, 404: "Category not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=category_update_body,
    responses={200: CategorySerializer, 400: "Invalid input", 404: "Category not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "Category not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
   
@swagger_auto_schema(
    method='post',
    request_body=subcategory_request_body,
    responses={201: SubCategorySerializer, 400: "Invalid input"}
)
@swagger_auto_schema(
    method='get',
    responses={200: SubCategorySerializer(many=True)}
)
@api_view(['GET', 'POST'])
def subcategory_view(request):
    if request.method == 'GET':
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response({"message": "Invalid data", "details": errors}, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
    method='get',
    responses={200: SubCategorySerializer(many=True), 404: "Category not found"}
)
@api_view(['GET'])
def subcategories_by_category(request, category_id):
    try:
        subcategories = SubCategory.objects.filter(category_id=category_id)
        if not subcategories.exists():
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@swagger_auto_schema(
    method='get',
    responses={200: SubCategorySerializer, 404: "SubCategory not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=subcategory_update_body,
    responses={200: SubCategorySerializer, 400: "Invalid input", 404: "SubCategory not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "SubCategory not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def subcategory_detail(request, pk):
    try:
        subcategory = SubCategory.objects.get(pk=pk)
    except SubCategory.DoesNotExist:
        return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subcategory.delete()
        return Response({'message': 'SubCategory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='get',
    responses={200: ArticleSerializer, 404: "Content not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=article_update_body,
    responses={200: ArticleSerializer, 400: "Invalid input", 404: "Content not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "Content not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        content = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({'error': 'Articles not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        print(f"Request Data: {request.data}") 
        serializer = ArticleSerializer(content, data=request.data)
        if serializer.is_valid():
            print(f"Validated Data: {serializer.validated_data}") 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(f"Check request errors: {serializer.errors}")  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        content.active = 0  
        content.save()  
        return Response({'message': 'Article set to inactive (active = 0)'}, status=status.HTTP_204_NO_CONTENT)
        
@swagger_auto_schema(
    method='post',
    request_body=ArticleSerializer,
    responses={
        201: openapi.Response("Content successfully created", ArticleSerializer),
        400: openapi.Response("Invalid input data"),
    }
)
@api_view(['POST'])
def article_create_by_subcategory(request):
    """
    API để tạo Article mới dựa trên SubCategory.
    """
    serializer = ArticleSerializer(data=request.data)

    try:
        if serializer.is_valid(raise_exception=True):  
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"errors": "Something went wrong.", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response("List of all Content", ArticleSerializer(many=True)),
        500: openapi.Response("Internal Server Error"),
    }
)
@api_view(['GET'])
def article_get_all(request):
    """
    API để lấy tất cả Articles.
    """
    try:
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"errors": "Something went wrong.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# views.py
@swagger_auto_schema(
    method='post',
    request_body=comment_request_body,
    responses={201: CommentSerializer, 400: "Invalid input"}
)
@swagger_auto_schema(
    method='get',
    responses={200: CommentSerializer(many=True)}
)
@api_view(['GET', 'POST'])
def comment_view(request, articles_id):  
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=articles_id)  
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        serializer = CommentSerializer(data=data)
        print(f"check params {request.query_params}")
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: CommentSerializer, 404: "Comment not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=comment_update_body,
    responses={200: CommentSerializer, 400: "Invalid input", 404: "Comment not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "Comment not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ViewSet, 
                  generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]