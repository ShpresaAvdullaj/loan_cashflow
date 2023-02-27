from django.db import models


class CashFlow(models.Model):
    loan_identifier = models.CharField(max_length=25)
    reference_date = models.DateField()
    type = models.CharField(max_length=86)
    amount = models.FloatField()
