# Generated by Django 4.2.7 on 2023-11-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=3000)),
                ('price', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
            ],
        ),
    ]