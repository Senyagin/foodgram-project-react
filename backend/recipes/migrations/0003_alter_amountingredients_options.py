# Generated by Django 3.2.15 on 2023-08-15 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amountingredients',
            options={'verbose_name': 'Ингредиент в рецепте', 'verbose_name_plural': 'Ингредиентов в рецепте'},
        ),
    ]
