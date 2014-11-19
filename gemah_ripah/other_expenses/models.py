from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class OtherExpenses(models.Model):
    date = models.DateField()
    remarks = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-date", "-id")

    def __str__(self):
        return "%s: %s: %f" % (self.date, self.remarks, self.amount)

