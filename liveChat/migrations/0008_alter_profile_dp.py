# Generated by Django 4.1 on 2022-10-09 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveChat', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
