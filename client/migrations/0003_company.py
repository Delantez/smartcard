# Generated by Django 5.1.3 on 2024-11-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_contact_qrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('product', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='media/company_qrcodes/')),
            ],
        ),
    ]
