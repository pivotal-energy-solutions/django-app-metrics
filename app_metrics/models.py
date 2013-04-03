import datetime

from django.conf import settings
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from app_metrics.managers import MetricManager
from apps.company.models import Company
from django.utils.timezone import now as utcnow

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Metric(models.Model):
    """ The type of metric we want to store """
    name = models.CharField(_('name'), max_length=32)
    company = models.ForeignKey(Company, blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=64, db_index=True)

    class Meta:
        unique_together = ('slug', 'company')
        verbose_name = _('metric')
        verbose_name_plural = _('metrics')

    def __unicode__(self):
        company = u'' if not self.company else u' ({})'.format(self.company)
        return u'{}{}'.format(self.name, company)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Metric, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s-%d" % (self.slug, i)
        else:
            return super(Metric, self).save(*args, **kwargs)

class MetricSet(models.Model):
    """ A set of metrics that should be sent via email to certain users """
    name = models.CharField(_('name'), max_length=50)
    metrics = models.ManyToManyField(Metric, verbose_name=_('metrics'))
    email_recipients = models.ManyToManyField(USER_MODEL, verbose_name=_('email recipients'))
    no_email = models.BooleanField(_('no e-mail'), default=False)
    send_daily = models.BooleanField(_('send daily'), default=True)
    send_weekly = models.BooleanField(_('send weekly'), default=False)
    send_monthly = models.BooleanField(_('send monthly'), default=False)

    class Meta:
        verbose_name = _('metric set')
        verbose_name_plural = _('metric sets')

    def __unicode__(self):
        return self.name

class MetricItem(models.Model):
    """ Individual metric items """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.IntegerField(_('number'), default=1)
    created = models.DateTimeField(_('created'), default=utcnow)

    class Meta:
        verbose_name = _('metric item')
        verbose_name_plural = _('metric items')

    def __unicode__(self):
        return _("'%(name)s' of %(num)d on %(created)s") % {
            'name': self.metric,
            'num': self.num,
            'created': self.created
        }

class MetricDay(models.Model):
    """ Aggregation of Metrics on a per day basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    objects = MetricManager()

    class Meta:
        verbose_name = _('day metric')
        verbose_name_plural = _('day metrics')

    def __unicode__(self):
        return _("'%(name)s' for '%(created)s'") % {
            'name': self.metric,
            'created': self.created
        }

class MetricWeek(models.Model):
    """ Aggregation of Metrics on a weekly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    objects = MetricManager()

    class Meta:
        verbose_name = _('week metric')
        verbose_name_plural = _('week metrics')

    def __unicode__(self):
        return _("'%(name)s' for week %(week)s of %(year)s") % {
            'name': self.metric,
            'week': self.created.strftime("%U"),
            'year': self.created.strftime("%Y")
        }

class MetricMonth(models.Model):
    """ Aggregation of Metrics on monthly basis """
    metric = models.ForeignKey(Metric, verbose_name=('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    objects = MetricManager()

    class Meta:
        verbose_name = _('month metric')
        verbose_name_plural = _('month metrics')

    def __unicode__(self):
        return _("'%(name)s' for %(month)s %(year)s") % {
            'name': self.metric,
            'month': self.created.strftime("%B"),
            'year': self.created.strftime("%Y")
        }


class MetricYear(models.Model):
    """ Aggregation of Metrics on a yearly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    objects = MetricManager()

    class Meta:
        verbose_name = _('year metric')
        verbose_name_plural = _('year metrics')

    def __unicode__(self):
        return _("'%(name)s' for %(year)s") % {
            'name': self.metric,
            'year': self.created.strftime("%Y")
        }


class Gauge(models.Model):
    """
    A representation of the current state of some data.
    """
    name = models.CharField(_('name'), max_length=32)
    company = models.ForeignKey(Company, blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=64)
    current_value = models.DecimalField(_('current value'), max_digits=15, decimal_places=6, default='0.00')
    created = models.DateTimeField(_('created'), default=utcnow)
    updated = models.DateTimeField(_('updated'), default=utcnow)

    class Meta:
        verbose_name = _('gauge')
        verbose_name_plural = _('gauges')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Gauge, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s-%d" % (self.slug, i)
        return super(Gauge, self).save(*args, **kwargs)
