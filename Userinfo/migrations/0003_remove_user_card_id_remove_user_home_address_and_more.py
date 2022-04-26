# Generated by Django 4.0.4 on 2022-04-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userinfo', '0002_rename_date_joined_user_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='card_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True, verbose_name='激活状态'),
        ),
    ]