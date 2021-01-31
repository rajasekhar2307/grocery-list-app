from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Grocery(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.CharField(max_length = 5)
    status = models.IntegerField()
    date_given = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
