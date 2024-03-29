# Generated by Django 2.2.28 on 2022-07-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variants', '0003_auto_20220706_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querymodel',
            name='variant_alt',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], default='A', max_length=50),
        ),
        migrations.AlterField(
            model_name='querymodel',
            name='variant_ref',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], default='A', max_length=50),
        ),
    ]
