# Generated by Django 4.2.3 on 2023-10-05 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cas',
            name='item_id',
            field=models.IntegerField(verbose_name='Transaction item ID no.'),
        ),
    ]
