# Generated by Django 5.1.3 on 2024-11-20 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_identity_validity_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='media/files/')),
            ],
        ),
    ]
