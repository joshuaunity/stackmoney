# Generated by Django 3.2.9 on 2021-11-20 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_transaction_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='phone',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='ref',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
