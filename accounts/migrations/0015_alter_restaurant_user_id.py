# Generated by Django 5.2 on 2025-04-22 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_orderitem_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]
