# Generated by Django 4.2.3 on 2023-09-03 08:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moonfish_recipe', '0003_remove_food_is_favorite_food_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
