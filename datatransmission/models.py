from django.db import models
from cas.models import Cas
from django.contrib.auth.models import User

# Create your models here.
class DataTransmission(models.Model):
    cas = models.ForeignKey(Cas, on_delete=models.SET_NULL, null=True, related_name='datatransmission_cas', db_index=True)
    STATUS_CHOICES = (
        ('0', 'Failure'),
        ('1', 'Success')
    )
    transfer_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')
    ref_submit_id = models.CharField(max_length=255, blank=True, null=True, default='')
    acknowledgement_id = models.CharField(max_length=255, blank=True, null=True, default='')
    response_datetime = models.CharField(max_length=50, blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    error_code = models.CharField(max_length=30, blank=True, null=True, default='')
    error_message = models.CharField(max_length=255, blank=True, null=True, default='')
    system_configuration_mode = models.CharField(max_length=20, default='')
    transmitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='datatransmission_transmitted')
    transmitted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_datatransmission'


class TokenModel(models.Model):
    auth_token = models.CharField(max_length=255, default='')
    session_key = models.CharField(max_length=255, default='')
    token_expiry = models.CharField(max_length=50, default='')
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='token_entered')
    entered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_token'
        verbose_name = "Token Model"
        verbose_name_plural = "Token Model"

    def save(self, *args, **kwargs):
        # Override the save method to ensure there's only one row
        self.id = 1
        super(TokenModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Custom method to load the single instance
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class InquiryResult(models.Model):
    datatransmission = models.ForeignKey(DataTransmission, on_delete=models.SET_NULL, default=1, null=True, related_name='inquiryresult_datatransmission', db_index=True)
    STATUS_CHOICES = (
        ('0', 'Failure'),
        ('1', 'Success')
    )
    transfer_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')
    acknowledgement_id = models.CharField(max_length=255, blank=True, null=True, default='')
    response_datetime = models.CharField(max_length=50, blank=True, null=True, default='')
    PROCESS_STATUS_CODE_CHOICES = (
        ('01', 'Processing completed'),
        ('02', 'In processing'),
        ('03', 'Unable to process'),
    )
    process_status_code = models.CharField(max_length=50, choices=PROCESS_STATUS_CODE_CHOICES, blank=True, null=True, default='')
    RESULT_STATUS_CODE_CHOICES = (
        ('SUC001', 'Success'),
        ('SYN002', 'Invalid signature'),
        ('SYN003', 'Duplicated EisUniqueId'),
        ('SYN004', 'e-invoice schema error'),
        ('ERR001', 'Seller TIN error'),
        ('ERR002', 'Issuance datetime error'),
        ('ERR003', 'Transmission datetime error'),
        ('ERR004', 'Total Sales Amount, VAT Amount error'),
        ('ERR005', 'Code type error'),
        ('ERR006', 'Accreditation ID error'),
        ('ERR007', 'E-invoice Unique ID to be corrected error'),
        ('ERR999', 'Other undefined error'),
    )
    result_status_code = models.CharField(max_length=50, choices=RESULT_STATUS_CODE_CHOICES, blank=True, null=True, default='')
    error_code = models.CharField(max_length=50, blank=True, null=True, default='')
    error_message = models.CharField(max_length=255, blank=True, null=True, default='')
    inquired_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='datatransmission_inquired')
    inquired_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_inquiryresult'
    