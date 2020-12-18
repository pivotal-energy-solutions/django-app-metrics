# -*- coding: utf-8 -*-
from django.db import models


class Relationship(models.Model):
    name = models.CharField(max_length=25)
