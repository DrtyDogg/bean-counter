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
