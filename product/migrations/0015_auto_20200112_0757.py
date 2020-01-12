# Generated by Django 3.0.2 on 2020-01-12 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20200109_0434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='c_order',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='sessions_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='products',
            name='customer',
        ),
        migrations.AddField(
            model_name='cart',
            name='c_total',
            field=models.DecimalField(decimal_places=2, max_digits=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='cart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Cart'),
        ),
        migrations.AddField(
            model_name='customer',
            name='products',
            field=models.ManyToManyField(blank=True, to='product.Products'),
        ),
        migrations.AddField(
            model_name='order',
            name='c_cart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Cart'),
        ),
    ]