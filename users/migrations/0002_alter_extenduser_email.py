# Generated by Django 3.2.12 on 2022-02-14 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email'),
        ),
    ]
