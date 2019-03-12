from collections import defaultdict, OrderedDict

from django.views.generic import TemplateView

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Agreement


class IndexView(TemplateView):
    template_name = "agreement/index.html"


class AgreementsCalendarAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        # default dict with default values is [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        date_dict = defaultdict(lambda: [0 for _ in range(12)])

        agreements = self.get_queryset()
        for agreement in agreements:
            period = agreement.periods.first()  # take first() because periods ordering '-stop_date'
            if period:
                date_dict[period.stop_date.year][period.stop_date.month - 1] += 1
        ordered_date_dict = OrderedDict(sorted(date_dict.items()))

        return Response(ordered_date_dict)

    def get_queryset(self):
        # initial queryset
        agreements = Agreement.objects.prefetch_related('periods')

        # filtering queryset by country
        country_params = self.request.query_params.get('country')
        if country_params:
            agreements = agreements.filter(
                company__country_id__in=self.validate_id_list(country_params.replace(',', ' ').split())
            )

        # filtering queryset by negotiator
        negotiator_params = self.request.query_params.get('negotiator')
        if negotiator_params:
            agreements = agreements.filter(
                negotiator_id__in=self.validate_id_list(negotiator_params.replace(',', ' ').split())
            )

        # filtering queryset by company
        company_params = self.request.query_params.get('company')
        if company_params:
            agreements = agreements.filter(
                company_id__in=self.validate_id_list(company_params.replace(',', ' ').split())
            )

        return agreements

    @staticmethod
    def validate_id_list(params_list):  # плохой костыль для проверки численных id, подумать еще!
        int_list = []
        for i in params_list:
            try:
                int_list.append(int(i))
            except ValueError:
                pass
        return int_list
