from collections import OrderedDict
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from apps.agreement.models import Agreement, Period, Company


class AgreementsViewsTests(APITestCase):

    fixtures = ('test_fixtures.json', )

    def setUp(self):
        self.client = APIClient()
        agr1 = Agreement.objects.create(
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 5, 12),
            company=Company.objects.get(id=4),
            negotiator=User.objects.get(id=2),
            debit=200,
            credit=400,
        )
        agr2 = Agreement.objects.create(
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 6, 12),
            company=Company.objects.get(id=2),
            negotiator=User.objects.get(id=1),
            debit=200,
            credit=400,
        )
        agr3 = Agreement.objects.create(
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 8, 12),
            company=Company.objects.get(id=3),
            negotiator=User.objects.get(id=3),
            debit=200,
            credit=400,
        )
        Period.objects.create(
            agreement=agr1,
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 5, 12),
            status='N',
        )
        Period.objects.create(
            agreement=agr2,
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 6, 12),
            status='N',
        )
        Period.objects.create(
            agreement=agr3,
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 8, 12),
            status='N',
        )

    def test_agreements_calendar_APIView(self):
        # without filters
        response = self.client.get(reverse('agreement:calendar'))
        self.assertEqual(
            response.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]})
        )

        # with country filter
        response_1country = self.client.get(reverse('agreement:calendar'), {'country': '1'})
        self.assertEqual(
            response_1country.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]})
        )
        response_some_country = self.client.get(reverse('agreement:calendar'), {'country': '2,5'})
        self.assertEqual(
            response_some_country.data,
            OrderedDict({2019: [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]})
        )

        # with negotiator filters
        response_1neg = self.client.get(reverse('agreement:calendar'), {'negotiator': '1'})
        self.assertEqual(
            response_1neg.data,
            OrderedDict({2019: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]})
        )
        response_some_neg = self.client.get(reverse('agreement:calendar'), {'negotiator': '2,3'})
        self.assertEqual(
            response_some_neg.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]})
        )

        # with company filter
        response_1comp = self.client.get(reverse('agreement:calendar'), {'company': '4'})
        self.assertEqual(
            response_1comp.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]})
        )
        response_some_comp = self.client.get(reverse('agreement:calendar'), {'company': '2,3'})
        self.assertEqual(
            response_some_comp.data,
            OrderedDict({2019: [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]})
        )

        # with some filters
        response_1 = self.client.get(reverse('agreement:calendar'), {'country': '1,5', 'negotiator': '1'})
        self.assertEqual(
            response_1.data,
            OrderedDict({2019: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]})
        )
        response_2 = self.client.get(
            reverse('agreement:calendar'),
            {'country': '1,2,5', 'company': '2,3', 'negotiator': '2'}
        )
        self.assertEqual(
            response_2.data,
            OrderedDict()
        )
        response_3 = self.client.get(
            reverse('agreement:calendar'),
            {'country': '1,2,5', 'company': '2,3,4', 'negotiator': '1,2'}
        )
        self.assertEqual(
            response_3.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]})
        )
        response_4 = self.client.get(
            reverse('agreement:calendar'),
            {'country': '1,2,5,bad', 'company': '2,query,3,4', 'negotiator': '1,param,2'}
        )
        self.assertEqual(
            response_4.data,
            OrderedDict({2019: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]})
        )
