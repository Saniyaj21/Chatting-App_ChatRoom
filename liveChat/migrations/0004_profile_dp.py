# Generated by Django 4.1 on 2022-10-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveChat', '0003_rename_dp_profile_user_profile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dp',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]