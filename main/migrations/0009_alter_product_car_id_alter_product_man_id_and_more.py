# Generated by Django 4.2.7 on 2023-11-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_product_prod_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='car_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='man_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_usd',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_year',
            field=models.IntegerField(),
        ),
    ]
