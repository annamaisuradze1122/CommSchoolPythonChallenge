# Generated by Django 4.2.7 on 2023-11-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_requestscrapper_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]