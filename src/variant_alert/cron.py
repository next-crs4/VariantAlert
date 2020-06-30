import os
import logging
from django_cron import CronJobBase, Schedule
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User

from apps.variants.models import QueryModel

from components.variants import Variants
from components.jsoncompare import compare
from django.utils.timezone import now


class QueryCronJob(CronJobBase):

    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'variant_alert.my_cron_job'    # a unique code

    def __alert(self, q):
        url = os.path.join(settings.HOST, 'variants', 'query', str(q.id))

        for u in User.objects.all():
            if u.id == q.user_id:
                self.logger.info('Preparing mail for user: {} - {}'.format(u.username, u.email))
                try:
                    email = EmailMessage(
                        "VariantAlert updates - {}".format(now()),
                        "Dear {}\n, Changes in annotations were detected for the following variant(s): {}: {}.\n"
                        "Go to {} for details. \nVariantAlert Team ".format(u.username, q.label, q.query, url),
                        to=[u.email])
                    email.send()
                    self.logger.info('Mail sent to user: {} - {}'.format(u.username, u.email))
                except Exception as e:
                    self.logger.error(e)

    def a_logger(self, name, level="INFO", filename=None, mode="a"):
        log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
        log_datefmt = '%Y-%m-%d %H:%M:%S'
        logger = logging.getLogger(name)
        if not isinstance(level, int):
            try:
                level = getattr(logging, level)
            except AttributeError:
                raise ValueError("unsupported literal log level: %s" % level)
            logger.setLevel(level)
        if filename:
            handler = logging.FileHandler(filename, mode=mode)
        else:
            handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format, datefmt=log_datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def do(self):
        self.logger = self.a_logger(self.__class__.__name__)
        self.logger.info('=== START ===')
        self.logger.info('Collecting Queries...')
        queries = QueryModel.objects.all()
        v = Variants()
        for q in queries:
            self.logger.info('Checking for changes in the query {} - user {}'.format(q.label, q.user_id))
            q.previous = q.result
            q.result = v.get_variant(q.query, q.assembly)
            q.difference = compare(q.previous, q.result)
            q.date = q.date
            if q.difference:
                self.logger.info('ALERT - Found change for query {} - user {}'.format(q.label, q.user_id))
                q.update = now()
                q.save()
                self.__alert(q)
            else:
                self.logger.info('Nothing is changed for query {} - user {}'.format(q.label, q.user_id))
             


