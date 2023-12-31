# Generated by Django 4.2.3 on 2023-09-21 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EisCredential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.TextField(verbose_name='Public Key')),
                ('user_id', models.CharField(max_length=255, verbose_name='User ID')),
                ('user_password', models.CharField(max_length=255, verbose_name='User Password')),
                ('application_id', models.CharField(max_length=255, verbose_name='Application ID')),
                ('application_secret_key', models.CharField(max_length=255, verbose_name='Application Secret Key')),
                ('accreditation_id', models.CharField(max_length=255, verbose_name='Accreditation ID or EIS Cert Number')),
                ('jws_key_id', models.CharField(max_length=255, verbose_name='JWS Key ID')),
                ('force_refresh_token', models.CharField(max_length=20, verbose_name='Force Refresh Token')),
                ('authorization_url', models.CharField(max_length=255, verbose_name='Authorization URL')),
                ('invoices_url', models.CharField(max_length=255, verbose_name='Authorization URL')),
                ('inquiry_result_url', models.CharField(max_length=255, verbose_name='Inquiry Result URL')),
                ('access_level', models.CharField(choices=[('U', 'UAT'), ('P', 'Production')], max_length=20, verbose_name='Access Level')),
                ('entered_by', models.IntegerField(default=1)),
                ('entered_date', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'eis_credential',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_eis_system_mode', models.CharField(choices=[('U', 'UAT'), ('P', 'Production')], max_length=20, verbose_name='EIS System Mode')),
                ('entered_by', models.IntegerField(default=1)),
                ('entered_date', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'setting',
                'ordering': ['-pk'],
            },
        ),
    ]
