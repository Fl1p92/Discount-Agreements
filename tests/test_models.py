from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from apps.agreement.models import Agreement, Period, Company, BadPeriodError


class AgreementsModelsTests(TestCase):

    fixtures = ('fixtures.json', )

    def setUp(self):
        self.agreement = Agreement.objects.create(
            start_date=date(2019, 1, 1),
            stop_date=date(2019, 12, 12),
            company=Company.objects.first(),
            negotiator=User.objects.first(),
            debit=200,
            credit=400,
        )

    def test_invalid_periods_dates_relatively_agreement(self):
        self.assertFalse(Period.objects.exists())

        # test period start_date validation
        bad_start_date_period = Period(
            agreement=self.agreement,
            start_date=date(2018, 1, 1),
            stop_date=date(2019, 12, 12),
            status='N',
        )
        with self.assertRaisesMessage(BadPeriodError,
                                      'Period start date must be later than start date of the agreement'):
            bad_start_date_period.save()

        # test period stop_date validation
        bad_stop_date_period = Period(
            agreement=self.agreement,
            start_date=date(2019, 1, 1),
            stop_date=date(2020, 1, 1),
            status='N',
        )
        with self.assertRaisesMessage(BadPeriodError,
                                      'Period stop date must be earlier than stop date of the agreement'):
            bad_stop_date_period.save()

        self.assertFalse(Period.objects.exists())

    def test_periods_intersection_check(self):
        # create initial period
        Period.objects.create(
            agreement=self.agreement,
            start_date=date(2019, 5, 5),
            stop_date=date(2019, 8, 8),
            status='N',
        )
        self.assertEqual(Period.objects.count(), 1)

        # start_date intersection
        start_date_intersection_period = Period(
            agreement=self.agreement,
            start_date=date(2019, 6, 6),
            stop_date=date(2019, 10, 10),
            status='N',
        )
        with self.assertRaisesMessage(BadPeriodError,
                                      'Period start date should not intersect with existing periods'):
            start_date_intersection_period.save()

        # stop_date intersection
        stop_date_intersection_period = Period(
            agreement=self.agreement,
            start_date=date(2019, 3, 3),
            stop_date=date(2019, 6, 6),
            status='N',
        )
        with self.assertRaisesMessage(BadPeriodError,
                                      'Period stop date should not intersect with existing periods'):
            stop_date_intersection_period.save()

        # total intersection
        total_intersection_period = Period(
            agreement=self.agreement,
            start_date=date(2019, 3, 3),
            stop_date=date(2019, 10, 10),
            status='N',
        )
        with self.assertRaisesMessage(BadPeriodError,
                                      'Period should not intersect with existing periods'):
            total_intersection_period.save()

        self.assertEqual(Period.objects.count(), 1)
