# Generated by Django 4.0.4 on 2022-04-22 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('IBSN', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
            ],
        ),
    ]
