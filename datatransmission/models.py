from django.db import models
from cas.models import Cas
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

    
    