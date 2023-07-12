# Generated by Django 4.2.2 on 2023-07-07 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_feestructure'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeePaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rollno', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField()),
            ],
        ),
    ]
