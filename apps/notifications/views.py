from django.views.generic import RedirectView

from .tasks import send_notifications


class SendMailView(RedirectView):
    pattern_name = 'agreement:calendar'

    def get(self, request, *args, **kwargs):
        send_notifications.delay()
        return super().get(request, *args, **kwargs)
