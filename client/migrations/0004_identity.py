# Generated by Django 5.1.3 on 2024-11-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=15)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('validity_time', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='media/qrcodes/')),
            ],
        ),
    ]