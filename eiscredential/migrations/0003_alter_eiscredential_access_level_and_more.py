# Generated by Django 4.2.3 on 2023-09-26 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eiscredential', '0002_alter_eiscredential_entered_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eiscredential',
            name='access_level',
            field=models.CharField(choices=[('Sandbox', 'UAT'), ('Live', 'Production')], max_length=20, verbose_name='Access Level'),
        ),
        migrations.AlterField(
            model_name='eiscredential',
            name='force_refresh_token',
            field=models.CharField(blank=True, default='false', max_length=20, null=True, verbose_name='Force Refresh Token'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='config_eis_system_mode',
            field=models.CharField(choices=[('Sandbox', 'UAT'), ('Live', 'Production')], max_length=20, verbose_name='EIS System Mode'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='entered_by',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eissetting_entered', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='setting',
            name='modified_by',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eissetting_modified', to=settings.AUTH_USER_MODEL),
        ),
    ]
