# Generated by Django 4.1 on 2022-10-14 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveChat', '0011_alter_profile_dp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(blank=True, default='bydefault.jpg', null=True, upload_to='media'),
        ),
    ]
