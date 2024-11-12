from app_metrics.tasks import db_metric_task, db_gauge_task


def metric(num=1, **kwargs):
    """Fire a celery task to record our metric in the database"""
    db_metric_task.delay(num, **kwargs)


def timing(seconds_taken, **kwargs):
    # Unsupported, hence the noop.
    pass


def gauge(current_value, **kwargs):
    """Fire a celery task to record the gauge's current value in the database."""
    db_gauge_task.delay(current_value, **kwargs)
