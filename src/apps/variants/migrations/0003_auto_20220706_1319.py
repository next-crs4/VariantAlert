# Generated by Django 2.2.28 on 2022-07-06 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variants', '0002_auto_20220706_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querymodel',
            name='variant_ref',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], default='A', max_length=10),
        ),
    ]
