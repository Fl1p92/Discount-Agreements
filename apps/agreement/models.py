from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class BadPeriodError(ValidationError): pass


class Agreement(models.Model):
    start_date = models.DateField('Start date')
    stop_date = models.DateField('Stop date')
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='agreements',
        verbose_name='Company',
    )
    negotiator = models.ForeignKey(
        'auth.User',
        on_delete=models.SET(get_sentinel_user),
        related_name='agreements',
        verbose_name='Negotiator',
    )
    debit = models.PositiveIntegerField('Debit')
    credit = models.PositiveIntegerField('Credit')

    class Meta:
        verbose_name = 'Agreement'
        verbose_name_plural = 'Agreements'

    def __str__(self):
        return f'Agreement #{self.id} concluded with {self.company.title}'


class Period(models.Model):
    PERIOD_STATUSES = (
        ('N', 'New'),
        ('A', 'Active'),
        ('R', 'Reconciliation'),
        ('C', 'Closed'),
    )

    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        related_name='periods',
        verbose_name='Agreement',
    )
    start_date = models.DateField('Start date')
    stop_date = models.DateField('Stop date')
    status = models.CharField('Status', max_length=1, choices=PERIOD_STATUSES)

    class Meta:
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
        ordering = ('-stop_date', )

    def __str__(self):
        return f'Period #{self.id} of agreement #{self.agreement.id}'

    def save(self, **kwargs):
        # start_date check
        if self.start_date < self.agreement.start_date:
            raise BadPeriodError('Period start date must be later than start date of the agreement')
        # stop_date check
        if self.stop_date > self.agreement.stop_date:
            raise BadPeriodError('Period stop date must be earlier than stop date of the agreement')

        # periods intersection check
        periods = self.agreement.periods.exclude(id=self.id)  # exclude prevents raise on update instance
        if periods.filter(start_date__lt=self.start_date, stop_date__gt=self.start_date).exists():
            raise BadPeriodError('Period start date should not intersect with existing periods')
        if periods.filter(start_date__lt=self.stop_date, stop_date__gt=self.stop_date).exists():
            raise BadPeriodError('Period stop date should not intersect with existing periods')
        if periods.filter(start_date__gt=self.start_date, stop_date__lt=self.stop_date).exists():
            raise BadPeriodError('Period should not intersect with existing periods')

        super().save(**kwargs)


class Company(models.Model):
    title = models.CharField('Title', max_length=200)
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE,
        related_name='companies',
        verbose_name='Country',
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f'"{self.title}" company from {self.country.name}'


class Country(models.Model):
    name = models.CharField('Name', max_length=200)
    code = models.CharField('3-alpha ISO code', max_length=3)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f'[{self.code}] {self.name}'
