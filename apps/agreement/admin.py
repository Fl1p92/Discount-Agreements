from django.contrib import admin

from . import models


class PeriodLineInline(admin.TabularInline):
    model = models.Period
    extra = 1


@admin.register(models.Agreement)
class AgreementAdmin(admin.ModelAdmin):
    inlines = (PeriodLineInline, )
    list_display = ('__str__', 'negotiator', 'start_date', 'stop_date', 'debit', 'credit')
    list_filter = ('negotiator', 'company', 'company__country')
    search_fields = ('id', 'negotiator__username', 'company__title', 'start_date', 'stop_date', 'debit', 'credit')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country')
    list_display_links = ('id', 'title')
    list_filter = ('country', )
    search_fields = ('id', 'title', 'country__code', 'country__name')


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = list_display_links = search_fields = ('id', 'code', 'name')
