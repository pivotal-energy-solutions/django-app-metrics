# -*- coding: utf-8 -*-

from django.urls import path

from app_metrics.views import MonthlyMetricReport, YearlyMetricReport, MetricReports

# Add these URLs to your main urlconf. Be sure to keep the namespace and app_name as `app_metrics`,
# the templates explicitly use them
# e.g.
#   (r'^metrics/', include('app_metrics.urls', namespace='app_metrics', app_name='app_metrics')),

app_name = 'app_metrics'
urlpatterns = [
    path('report/yearly/<int:year>/', YearlyMetricReport.as_view(),
         name='yearly_metric_report'),
    path('report/monthly/<str:month>/<int:year>/', MonthlyMetricReport.as_view(),
         name='monthly_metric_report'),
    path(r'reports/', MetricReports.as_view(), name='metric_reports'),
]
