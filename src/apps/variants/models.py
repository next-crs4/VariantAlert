from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField

from django.utils.timezone import now


# Create your models here.

class QueryModel(models.Model):
    chr_range = range(1, 23)
    CHR_CHOICE = [('chr' + str(i), 'chr' + str(i)) for i in chr_range]
    CHR_CHOICE.extend([('chrX', 'chrX'), ('chrY', 'chrY')])

    VARIANTS_CHOICE = [
        ('A', 'A'),
        ('C', 'C'),
        ('G', 'G'),
        ('T', 'T'),
    ]

    ASSEMBLY_CHOICE = [
        ('hg19', 'hg19'),
        ('hg38', 'hg38'),
    ]

    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    label = models.CharField(max_length=50, blank=True)
    chromosome = models.CharField(max_length=5, choices=CHR_CHOICE, default='1')
    position = models.PositiveIntegerField(blank=True)
    variant_ref = models.CharField(max_length=1, choices=VARIANTS_CHOICE, default='A')
    variant_alt = models.CharField(max_length=1, choices=VARIANTS_CHOICE, default='A')
    assembly = models.CharField(max_length=5, choices=ASSEMBLY_CHOICE, default='hg19')
    query = models.CharField(max_length=25, blank=True)
    result = JSONField(default=dict, blank=True)
    previous = JSONField(default=dict, blank=True)
    difference = JSONField(default=list, blank=True)
    fields = ArrayField(models.CharField(max_length=50, blank=True), default=list, blank=True)
    date = models.DateTimeField(default=now, blank=True)
    update = models.DateTimeField(default=now, blank=True)
    alert = models.BooleanField(default=False, blank=True)
