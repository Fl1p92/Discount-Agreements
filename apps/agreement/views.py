from collections import defaultdict, OrderedDict

from django.views.generic import TemplateView
from django.db.models import Max
from django.db.models.functions import ExtractYear, ExtractMonth

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Agreement


class IndexView(TemplateView):
    template_name = "agreement/index.html"


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter): pass


class AgreementFilter(filters.FilterSet):
    country = NumberInFilter(field_name='company__country_id', lookup_expr='in')
    negotiator = NumberInFilter(field_name='negotiator_id', lookup_expr='in')
    company = NumberInFilter(field_name='company_id', lookup_expr='in')

    class Meta:
        model = Agreement
        fields = ['country', 'negotiator', 'company']


class AgreementsCalendarAPIView(ListAPIView):

    queryset = Agreement.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AgreementFilter

    def list(self, request, *args, **kwargs):
        # default dict with default values is [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        date_dict = defaultdict(lambda: [0 for _ in range(12)])

        agreements = self.filter_queryset(self.get_queryset())
        agreements = agreements.annotate(
            stop=Max('periods__stop_date')
        ).annotate(
            year=ExtractYear('stop'),
            month=ExtractMonth('stop'),
        ).values('year', 'month')
        for agreement in agreements:
            date_dict[agreement['year']][agreement['month'] - 1] += 1
        ordered_date_dict = OrderedDict(sorted(date_dict.items()))

        return Response(ordered_date_dict)
