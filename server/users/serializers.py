from rest_framework import serializers
from .models import User, Category, SubCategory, Article, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password','phone', 'birthday', 'address', 'description', 'is_staff']
        write_only_fields = ['password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class SubCategorySerializer(serializers.ModelSerializer):
    sub = serializers.CharField(source='name')  
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = ['id', 'sub', 'description', 'category']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_date', 'updated_date', 'subcategories']

class ArticleSerializer(serializers.ModelSerializer):
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(),
        source='subcategory',
        write_only=False
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=False
    )

    image_url = serializers.URLField(required=False, allow_null=True)
    image_file = serializers.ImageField(required=False, allow_null=True)
    author = serializers.CharField(write_only=False)  

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'image_url',
            'image_file',
            'content',
            'author',  
            'created_date',
            'updated_date',
            'subcategory_id',
            'category_id',
            'active',
            'views',
        ]

    def validate(self, data):
        image_url = data.get('image_url')
        image_file = data.get('image_file')
        if image_url and image_file:
            raise serializers.ValidationError("Chỉ được cung cấp một trong hai: image_url hoặc image_file.")
        if not image_url and not image_file:
            raise serializers.ValidationError("Cần phải cung cấp ít nhất một trong hai: image_url hoặc image_file.")
        
        return data

    def create(self, validated_data):
        author_name = validated_data.pop('author', None)
        article = Article.objects.create(author=author_name, **validated_data)
        
        return article

class CommentSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'title', 'author', 'created_date', 'updated_date', 'active', 'article']