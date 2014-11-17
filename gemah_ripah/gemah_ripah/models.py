from django.db import models


class CharUpperCaseField(models.CharField):
    def get_prep_value(self, value):
        if not value:
            return value
        return value.upper()
