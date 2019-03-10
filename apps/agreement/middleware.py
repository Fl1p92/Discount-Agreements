from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from .models import BadPeriodError


class BadPeriodMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, BadPeriodError):
            return render(request, 'agreement/bad_period.html', {'message': exception.message})
