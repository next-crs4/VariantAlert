# Generated by Django 2.2.28 on 2022-07-06 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variants', '0004_auto_20220706_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querymodel',
            name='variant_alt',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], default='A', max_length=100),
        ),
    ]