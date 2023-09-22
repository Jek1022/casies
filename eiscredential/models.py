from django.db import models

# Create your models here.
class EisCredential(models.Model):
    public_key = models.TextField(verbose_name='Public Key')
    user_id = models.CharField(max_length=255, verbose_name='User ID')
    user_password = models.CharField(max_length=255, verbose_name='User Password')
    application_id = models.CharField(max_length=255, verbose_name='Application ID')
    application_secret_key = models.CharField(max_length=255, verbose_name='Application Secret Key')
    accreditation_id = models.CharField(max_length=255, verbose_name='Accreditation ID or EIS Cert Number')
    jws_key_id = models.CharField(max_length=255, verbose_name='JWS Key ID')
    force_refresh_token = models.CharField(max_length=20, verbose_name='Force Refresh Token')
    authorization_url = models.CharField(max_length=255, verbose_name='Authorization URL')
    invoices_url = models.CharField(max_length=255, verbose_name='Authorization URL')
    inquiry_result_url = models.CharField(max_length=255, verbose_name='Inquiry Result URL')
    ACCESS_LEVEL_CHOICES = (
        ('U', 'UAT'),
        ('P', 'Production')
    )
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, verbose_name='Access Level')
    entered_by = models.IntegerField(default=1)
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(default=1)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        db_table = 'eis_credential'
        ordering = ['-pk']

class Setting(models.Model):
    CONFIG_EIS_SYSTEM_MODE_CHOICES = (
        ('U', 'UAT'),
        ('P', 'Production')
    )
    config_eis_system_mode = models.CharField(max_length=20, choices=CONFIG_EIS_SYSTEM_MODE_CHOICES, verbose_name='EIS System Mode')
    entered_by = models.IntegerField(default=1)
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(default=1)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'setting'
        ordering = ['-pk']