# -*- coding: utf-8 -*-
"""managers.py: Django app_metrics"""

from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import models
from django.db.models import Q

__author__ = 'Steven Klass'
__date__ = '4/3/13 5:26 AM'
__copyright__ = 'Copyright 2012 Pivotal Energy Solutions. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)


class MetricManager(models.Manager):

    def filter_by_company(self, company, **kwargs):
        """A way to trim down the list of objects by company"""
        Company = apps.get_model('company', 'Company')
        assert isinstance(company, Company), 'Need a Company'
        return self.filter(metric__company=company, **kwargs)

    def filter_by_user(self, user, **kwargs):
        """A way to trim down the list of objects by user"""
        if user.is_superuser:
            return self.filter(**kwargs)
        kwargs['company'] = user.profile.company
        return self.filter_by_company(**kwargs)

    def filter_certifications_by_user(self, user, **kwargs):
        """A way to trim down the list of objects by company"""

        name = kwargs.pop('name', None)
        names = [name] if name else []
        if not len(names):
            EEPProgram = apps.get_model('eep_program', 'EEPProgram')
            names = EEPProgram.objects.filter_by_user(user).values_list('name', flat=True)
            names = ['EEP {} Certifications'.format(name) for name in names]

        if user.is_superuser:
            return self.filter(metric__name__in=names, **kwargs)
        company = user.company
        if company.company_type in ['rater', 'hvac', 'qa', 'provider']:
            return self.filter(metric__company=company, metric__name__in=names, **kwargs)

        # Everyone else should only see data for companies in which we have mutual relationships.
        Relationship = apps.get_model('relationship', 'Relationship')
        comps = Relationship.objects.get_reversed_companies(company, ids_only=True)
        # Who do I have a relationship with
        rels = company.relationships.get_companies(ids_only=True)
        # The intersection of these is what matters..
        ints = list(set(rels).intersection(set(comps)))
        data = self.filter(Q(metric__company=company) | Q(metric__company__in=ints),
                           metric__name__in=names, **kwargs)
        return data
