# Generated by Django 5.2.3 on 2025-07-18 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_taskdetail_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='asset',
            field=models.ImageField(blank=True, default='tasks_asset/default_img.png', null=True, upload_to='tasks_asset'),
        ),
    ]
