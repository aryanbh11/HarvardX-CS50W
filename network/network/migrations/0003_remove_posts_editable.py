# Generated by Django 3.1.5 on 2021-02-07 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210207_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='editable',
        ),
    ]
