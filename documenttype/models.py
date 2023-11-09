from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class DocumentType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=250)
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('C', 'Cancelled'),
        ('O', 'Posted'),
        ('P', 'Printed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='documenttype_entered')
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='documenttype_modified')
    modified_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'documenttype'
        ordering = ['-pk']
        
    def get_absolute_url(self):
        return reverse('documenttype:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def status_verbose(self):
        return dict(DocumentType.STATUS_CHOICES)[self.status]
    