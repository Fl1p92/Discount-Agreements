from collections import defaultdict, OrderedDict

from django.views.generic import TemplateView
from django.db.models import Max, Count
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
        agreements = self.filter_queryset(self.get_queryset())

        # date_dict = self.realization_one(agreements)
        date_dict = self.realization_two(agreements)

        ordered_date_dict = OrderedDict(sorted(date_dict.items()))
        return Response(ordered_date_dict)

    def realization_one(self, agreems):
        # default dict with default values is [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        date_dict = defaultdict(lambda: [0 for _ in range(12)])
        agreements = agreems.annotate(
            year=ExtractYear(Max('periods__stop_date')),
            month=ExtractMonth(Max('periods__stop_date')),
        ).values('year', 'month')
        for agreement in agreements:
            date_dict[agreement['year']][agreement['month'] - 1] += 1
        return date_dict

    def realization_two(self, agreems):
        date_dict = {}
        agreements = agreems.annotate(
            year=ExtractYear(Max('periods__stop_date')),
            month=ExtractMonth(Max('periods__stop_date')),
        ).values(
            'year',
            'month'
        ).annotate(
            count=Count('month')
        ).values(
            'year',
            'month',
            'count'
        )
        print(agreements)
        for agreement in agreements:
            date_dict[agreement['year']][agreement['month'] - 1] = agreement['count']
        return date_dict

###--------------------------------------------------- SQL ---------------------------------------------------###
# SELECT alias.year as year, alias.month as month, count(*) as count
# FROM (SELECT EXTRACT('month' FROM MAX(ap.stop_date)) as month, EXTRACT('year' FROM MAX(ap.stop_date)) as year
#       FROM agreement_agreement aa left join agreement_period ap on aa.id = ap.agreement_id
#       GROUP BY aa.id) as alias
# GROUP BY alias.year, alias.month;
#################################################################################################################
