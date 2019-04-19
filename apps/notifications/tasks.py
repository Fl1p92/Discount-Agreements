import logging
from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Max, Count
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string

from apps.agreement.models import Agreement
from discount.celery import app


@app.task
def send_notifications():
    current_month_agreements = Agreement.objects.annotate(
        current_month=ExtractMonth(Max('periods__stop_date'))
    ).filter(
        current_month=date.today().month
    ).aggregate(
        current_agreements_count=Count('current_month')
    )
    message = render_to_string('notifications/mail.html', {'agreements_count': current_month_agreements, })
    send_mail(
        ("Agreements calendar"),
        message,
        None,
        settings.MAIL_RECEIVER_LIST,
    )
    logging.info(f"Mail send to {settings.MAIL_RECEIVER_LIST} with result {current_month_agreements['current_agreements_count']}.")


###--------------------------------------------- SQL ---------------------------------------------###
# SELECT COUNT(alias.month) as current_agreements_count1
# FROM (SELECT EXTRACT('month' FROM MAX(ap.stop_date)) as month
#       FROM agreement_agreement aa left join agreement_period ap on aa.id = ap.agreement_id
#       GROUP BY aa.id) as alias
# WHERE alias.month = 5;
#
#
# SELECT COUNT(alias.month) as current_agreements_count2
# FROM (SELECT EXTRACT('month' FROM MAX(ap.stop_date)) as month
#       FROM agreement_agreement aa left join agreement_period ap on aa.id = ap.agreement_id
#       GROUP BY aa.id
#       HAVING EXTRACT('month' FROM MAX(ap.stop_date)) = 5) as alias;
#####################################################################################################

 # celery worker -A discount --loglevel=debug --concurrency=4
