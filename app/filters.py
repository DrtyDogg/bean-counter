from datetime import datetime
# Local imports
from app import app


@app.template_filter('date')
def format_date(date):
    """ Fomat a date as m/d/y """
    return date.strftime('%m/%d/%Y')


@app.template_filter('dollars')
def format_dollars(amount):
    """ format a float as $0.00 """
    return '${:,.2f}'.format(amount)


@app.template_filter('week_of')
def format_week_of(week):
    # Get the datetime object from
    start_day = datetime.strptime('2019w{} SUN'.format(week), '%YW%U %a')
    return start_day.strftime('Week of %a %B %d %Y')
