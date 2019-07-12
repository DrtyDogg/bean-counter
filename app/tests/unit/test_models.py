from datetime import datetime

"""
    Test cases for the models
"""


def test_category(new_category):
    assert new_category.title == 'New Category'
    assert new_category.budget_amount == 25.20


def test_lineitem(new_lineitem):
    date = datetime.strptime('07/11/2019', "%m/%d/%Y")
    assert new_lineitem.amount == 10.11
    assert new_lineitem.date == date
    assert new_lineitem.week == date.isocalendar()[1]
    assert new_lineitem.location == 'Home'
    assert new_lineitem.description == 'A description'
    assert new_lineitem.category_id == 1
