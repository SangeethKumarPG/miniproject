# Generated by Django 4.2.2 on 2023-07-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_feepaymentdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feepaymentdetail',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
