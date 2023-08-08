import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auc.settings')
app = Celery('auc', backend="rpc://", broker="redis://0.0.0.0:6379/1")
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
