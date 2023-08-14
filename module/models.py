from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class Module(models.Model):
    mainmodule = models.ForeignKey('mainmodule.Mainmodule', on_delete=models.CASCADE, related_name='mainmodule_id', validators=[MinValueValidator(1)])
    django_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='django_content_type_id', default=1, validators=[MinValueValidator(1)])
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=250)
    segment = models.CharField(max_length=50, unique=True)
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('C', 'Cancelled'),
        ('O', 'Posted'),
        ('P', 'Printed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='module_entered')
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='module_modified')
    modified_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'module'
        ordering = ['-pk']

    def get_absolute_url(self):
        return reverse('module:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    def status_verbose(self):
        return dict(Module.STATUS_CHOICES)[self.status]
