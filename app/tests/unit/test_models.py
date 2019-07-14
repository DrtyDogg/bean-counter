from datetime import datetime

from app.models import LineItem

"""
    Test cases for the models
"""


def test_category(new_category):
    assert new_category.title == 'New Category'
    assert new_category.budget_amount == 25.20


def test_lineitem(new_lineitem):
    """
        Test creating a LineItem with a string
    """
    date = datetime.strptime('07/11/2019', "%m/%d/%Y")
    assert new_lineitem.amount == 10.11
    assert new_lineitem.date == date
    assert new_lineitem.week == date.isocalendar()[1]
    assert new_lineitem.location == 'Home'
    assert new_lineitem.description == 'A description'
    assert new_lineitem.category_id == 1


def test_lineitem_withdate():
    """
        Test creating a LineItem using a date
    """
    date = datetime.strptime('07/11/2019', "%m/%d/%Y").date()
    new_lineitem = LineItem(10.11, date, 'Home', 'A description', 1)
    assert new_lineitem.amount == 10.11
    assert new_lineitem.date == date
    assert new_lineitem.week == date.isocalendar()[1]
    assert new_lineitem.location == 'Home'
    assert new_lineitem.description == 'A description'
    assert new_lineitem.category_id == 1
