# Generated by Django 5.1.5 on 2025-03-15 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=15),
        ),
    ]
