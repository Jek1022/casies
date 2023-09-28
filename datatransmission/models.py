from django.db import models
from cas.models import Cas
from django.contrib.auth.models import User

# Create your models here.
class DataTransmissionModel(Cas):
    TRANSFER_STATUS_CHOICES = (
        ('P', 'Processing'),
        ('T', 'Transmitted'),
        ('F', 'Failed'),
    )
    transfer_status = models.CharField(max_length=1, choices=TRANSFER_STATUS_CHOICES, default='A')

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


    
    