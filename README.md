# Discount Agreements 

## Description

### General

Module designed for analysis of discount conditions between partner companies.

Notion 1 - Discount Agreement (Agreement)
Notion 2 - Period of agreement (Period)
Notion 3 - Company
Notion 4 - Country
Notion 5 - Responsible person (Negotiator)

Agreement has start and stop date, company agreement concluded with, responsible person - negotiator, debit and credit turnover (export/import).

Period - start and stop date, status - state of a period. Could be: New, Active, Reconciliation, Closed.
One agreement have several periods inside.
Inside agreement periods  not intersect.
Agreement start date can be earlier than start date of the earliest period (but not vice versa) as well as agreement stop date can be later than stop date of the latest period (but not vice versa).

Company - title, country.

Country - 3-alpha iso code, name

Negotiator - a django user who is responsible for agreement.

### Admin interface 

Each object represented in Django admin.
Was provided search, filters etc.
Agreement display Periods with tabular inline.

### API

Was implement API for agreement calendar.

Number displayed in a month block means number of agreements that are closing this month.
Agreement is closing this month if stop date of latest period is in this month.

/agreements/calendar/ - sample JSON response:
```json
{
      "2017": [0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 0, 5],
      "2018": [1, 0, 0, 4, 0, 0, 0, 1, 7, 10, 0, 4]
}
```
2017 and 2018 are years.
Arrays - index means month number, digit - number of closing agreements.

Endpoint support following filters: country, negotiator, company.
For example: ?country=1,2,7&negotitator=4,8
Number is an id of an object.

---

##### In this project was used:
* Unit tests
* djangorestframework - `a powerful and flexible toolkit for building Web APIs.`
* django-environ - `allows you to use Twelve-factor methodology to configure your Django application with environment variables.`
* django-debug-toolbar - `a configurable set of panels that display various debug information about the current request/response.`
* django-filter - `a generic system for filtering Django QuerySets based on user selections.`
* django-widget-tweaks - `tweak the form field rendering in templates, not in python-level form definitions.`
* ipython - `is a command shell for interactive computing, that offers introspection, rich media, shell syntax, tab completion, and history. `
* pip-tools - `a set of command line tools to help you keep your pip-based packages fresh.`
* psycopg2 - `python-PostgreSQL Database Adapter.`
* celery - `is an open source asynchronous task queue or job queue which is based on distributed message passing.`
* redis - `is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker.`