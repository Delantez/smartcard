# Generated by Django 5.1.3 on 2024-11-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='media/qrcodes/'),
        ),
    ]
