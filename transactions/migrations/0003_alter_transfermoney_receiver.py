# Generated by Django 4.2.7 on 2023-12-29 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transfermoney'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfermoney',
            name='receiver',
            field=models.DecimalField(decimal_places=0, max_digits=6),
        ),
    ]
