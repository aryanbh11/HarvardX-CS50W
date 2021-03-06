# Generated by Django 3.1.5 on 2021-01-24 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210124_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.categories'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
