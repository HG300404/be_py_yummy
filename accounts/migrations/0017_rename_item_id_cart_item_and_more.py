# Generated by Django 5.2 on 2025-04-22 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_rename_restaurant_dish_restaurant_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='restaurant_id',
            new_name='restaurant',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='restaurant_id',
            new_name='restaurant',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='restaurant_id',
            new_name='restaurant',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='restaurant_id',
            new_name='restaurant',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='user_id',
            new_name='user',
        ),
    ]
