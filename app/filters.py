from datetime import datetime
from flask import current_app


@current_app.template_filter('date')
def format_date(date):
    """ Fomat a date as m/d/y """
    return date.strftime('%m/%d/%Y')


@current_app.template_filter('dollars')
def format_dollars(amount):
    """ format a float as $0.00 """
    return '${:,.2f}'.format(amount)


@current_app.template_filter('week_of')
def format_week_of(date):
    """ format a date coming in as weeknumber.year.startday and return
    'Week of startday """
    view = convert_date(date)
    return view.strftime('Week of %a %B %d %Y')


@current_app.template_filter()
def format_percentage(pct):
    """ trims a number to 2 decimal places """
    return round(pct, 2)


def convert_date(date):
    out = datetime.strptime(date, '%U.%Y.%a')
    return out
