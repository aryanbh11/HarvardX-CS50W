# Generated by Django 3.1.5 on 2021-01-24 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210123_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
