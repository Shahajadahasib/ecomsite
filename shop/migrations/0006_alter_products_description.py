# Generated by Django 3.2.6 on 2021-08-08 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_rename_neme_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]