# Generated by Django 3.2.9 on 2021-11-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_transaction_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='address',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
