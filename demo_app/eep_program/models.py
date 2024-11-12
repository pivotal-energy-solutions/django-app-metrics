from django.db import models


class EEProgram(models.Model):
    name = models.CharField(max_length=25)
