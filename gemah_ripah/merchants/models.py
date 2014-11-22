from django.contrib.auth.models import User
from django.db import models

from gemah_ripah.models import CharUpperCaseField


class Merchant(models.Model):
    code = CharUpperCaseField(max_length=2, unique=True)
    name = CharUpperCaseField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, blank=True, null=True, editable=False)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.name


