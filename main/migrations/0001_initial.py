# Generated by Django 5.2.4 on 2025-07-23 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('rating_rate', models.FloatField()),
                ('rating_count', models.IntegerField()),
            ],
        ),
    ]
