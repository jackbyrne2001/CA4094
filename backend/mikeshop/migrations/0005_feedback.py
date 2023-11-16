# Generated by Django 4.1.3 on 2023-10-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mikeshop', '0004_order_shipping_addr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('details', models.TextField()),
                ('satisfy', models.BooleanField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mikeshop.product')),
            ],
        ),
    ]
