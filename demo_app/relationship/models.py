from django.db import models


class Relationship(models.Model):
    name = models.CharField(max_length=25)
