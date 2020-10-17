import os
import logging
from django_cron import CronJobBase, Schedule
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User

from apps.variants.models import QueryModel

from components.variants import Variants
from components.toolkit import Toolkit
from django.utils.timezone import now


class QueryCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'variant_alert.my_cron_job'  # a unique code

    def __alert(self, u, queries):
        self.logger.info('Preparing mail for user: {} - {}'.format(u.get('username'), u.get('email')))
        msgs = "\n"
        base_url = os.path.join('http://'+settings.HOST, 'variants', 'query')
        for q in queries:
            url = os.path.join(base_url, str(q.id))
            msgs = msgs + "\t" + q.label + " - " + q.query + " (Go to {} for details)\n".format(url)

        subject = "VariantAlert updates - {}".format(now())
        body = "Dear {},\n".format(u.get('username')) \
               + "Changes in annotations were detected for the following variant(s):\n " \
               + msgs + "\nBest Regards\nThe VariantAlert Team ({})".format(settings.EMAIL_HOST_USER)
        try:
            email = EmailMessage(from_email=settings.EMAIL_HOST_USER,
                                 subject=subject, body=body, to=[u.get('email')])
            email.send()
            self.logger.info('Mail sent to user: {} - {}'.format(u.get('username'), u.get('email')))
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
        v = Variants()
        self.logger = self.a_logger(self.__class__.__name__)
        self.logger.info('=== START ===')
        self.logger.info('Collecting Users...')
        for u in User.objects.values():
            self.logger.info("Collecting Queries for {} - {}".format(u.get('username'), u.get('email')))
            alerts = list()
            queries = QueryModel.objects.filter(user_id=u.get('id'))
            for q in queries:
                self.logger.info('Checking for changes in the query {} - {}'.format(q.label, q.query))
                q.previous = q.result
                q.result = v.get_variant(q.query, q.assembly, q.fields)
                q.difference = Toolkit().compare(q.previous, q.result)
                q.date = q.date
                if q.difference:
                    self.logger.info('ALERT - Found change for query {} - {}'.format(q.label, q.query))
                    q.update = now()
                    q.save()
                    alerts.append(q)
                else:
                    self.logger.info('Nothing is changed for query {} - {}'.format(q.label, q.query))
            if alerts:
                self.__alert(u, alerts)

        self.logger.info('=== END ===')
