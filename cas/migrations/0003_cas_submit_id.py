# Generated by Django 4.2.3 on 2023-10-10 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cas', '0002_alter_cas_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cas',
            name='submit_id',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
