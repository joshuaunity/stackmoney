# Generated by Django 3.2.9 on 2021-11-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20211120_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='address',
            field=models.CharField(default='123, Saint mark Street', max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='phone',
            field=models.IntegerField(default='0701234803', null=True),
        ),
    ]