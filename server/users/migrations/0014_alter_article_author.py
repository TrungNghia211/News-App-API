# Generated by Django 5.1.3 on 2024-12-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_article_views_alter_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(default='Unknown Author', max_length=255),
        ),
    ]
