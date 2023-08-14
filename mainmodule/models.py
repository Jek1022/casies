from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Mainmodule(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=250)
    sort_number = models.IntegerField(blank=True, null=True, \
        validators=[MaxValueValidator(99), MinValueValidator(0)])
    DIVISION_CHOICES = (
        ('0', 'Overview Panel'),
        ('1', 'Operations'),
        ('2', 'Management Tools'),
    )
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, default='2')
    icon_file = models.CharField(max_length=50, blank=True, null=True)
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('C', 'Cancelled'),
        ('O', 'Posted'),
        ('P', 'Printed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='mainmodule_entered')
    entered_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True, related_name='mainmodule_modified')
    modified_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'mainmodule'
        ordering = ['-pk']

    def get_absolute_url(self):
        return reverse('mainmodule:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code
    
    def division_verbose(self):
        return dict(Mainmodule.DIVISION_CHOICES)[self.division]

    def status_verbose(self):
        return dict(Mainmodule.STATUS_CHOICES)[self.status]
