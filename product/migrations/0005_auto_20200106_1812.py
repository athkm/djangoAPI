# Generated by Django 3.0.2 on 2020-01-06 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_delete_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='customer',
            field=models.ManyToManyField(to='product.Customer'),
        ),
        migrations.RemoveField(
            model_name='bill',
            name='product',
        ),
        migrations.AddField(
            model_name='bill',
            name='product',
            field=models.ManyToManyField(to='product.Products'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='o_user',
        ),
        migrations.AddField(
            model_name='order',
            name='o_user',
            field=models.ManyToManyField(to='product.Customer'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='o_vender',
        ),
        migrations.AddField(
            model_name='order',
            name='o_vender',
            field=models.ManyToManyField(to='product.Vender'),
        ),
        migrations.RemoveField(
            model_name='products',
            name='vender',
        ),
        migrations.AddField(
            model_name='products',
            name='vender',
            field=models.ManyToManyField(to='product.Vender'),
        ),
    ]
