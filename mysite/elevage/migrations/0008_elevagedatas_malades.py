# Generated by Django 4.2 on 2025-05-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevage', '0007_merge_20250428_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='elevagedatas',
            name='malades',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
