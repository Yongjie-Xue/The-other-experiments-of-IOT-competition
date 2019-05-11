from django.db import models

class HistoryValue(models.Model):
    light = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)