import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auc.settings')
app = Celery('auc', backend="rpc://", broker="redis://auction-celery:6379/0")
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
