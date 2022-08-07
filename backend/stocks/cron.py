from django_cron import CronJobBase, Schedule
import requests
from .models import Stock


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 5 minutes
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'news.my_cron_job'

    def do(self):
        for stock in Stock.objects.all():
            stock.dummy +=1 
            