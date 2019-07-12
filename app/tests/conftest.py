import pytest

# Local imports
from app.models import Category, LineItem


@pytest.fixture(scope='module')
def new_category():
    new_category = Category('New Category', 25.20)
    return new_category


@pytest.fixture(scope='module')
def new_lineitem():
    new_lineitem = LineItem(10.11, '07/11/2019', 'Home', 'A description', 1)
    return new_lineitem
