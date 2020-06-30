from django.db import models 
from django.core.validators import MaxValueValidator, MinValueValidator

class Query(models.Model):
    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    chr = IntegerRangeField(min_value=1, max_value=50)
