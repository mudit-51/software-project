import pytest
from unittest.mock import Mock
from ..sales import Sales


@pytest.fixture
def mock_medicine():
    med = Mock()
    med.name = "Amoxicillin"
    med.identifier = "amoxicillin_001"
    med.price = 25.0
    med.toJson.return_value = {
        "name": "Amoxicillin",
        "identifier": "amoxicillin_001",
        "price": 25.0
    }
    return med


@pytest.fixture
def mock_cart(mock_medicine):
    cart = Mock()
    cart.get_cart.return_value = {mock_medicine: 2}
    cart.get_cart_json.return_value = [{
        "name": "Amoxicillin",
        "identifier": "amoxicillin_001",
        "price": 25.0,
        "quantity": 2,
        "total_price": 50.0
    }]
    return cart


def test_sales_initialization():
    sales = Sales()
    assert sales.sales_list == []


def test_add_sale_valid(mock_cart):
    sales = Sales()
    sales.add_sale(mock_cart)
    assert len(sales.sales_list) == 1
    assert sales.sales_list[0] == mock_cart


def test_add_sale_invalid():
    sales = Sales()
    with pytest.raises(ValueError, match="Cart object cannot be None"):
        sales.add_sale(None)


def test_get_sales_statistics(mock_cart, mock_medicine):
    sales = Sales()
    sales.add_sale(mock_cart)

    stats = sales.get_sales_statistics()
    assert len(stats) == 1
    assert stats[0]["identifier"] == "amoxicillin_001"
    assert stats[0]["quantity_sold"] == 2
    assert stats[0]["value_sold"] == 50.0


def test_get_sales_history_json(mock_cart):
    sales = Sales()
    sales.add_sale(mock_cart)
    history = sales.get_sales_history_json()
    assert isinstance(history, list)
    assert history[0][0]["name"] == "Amoxicillin"
    assert history[0][0]["quantity"] == 2
