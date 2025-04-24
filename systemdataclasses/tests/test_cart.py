import pytest
from unittest.mock import Mock
from ..cart import Cart


@pytest.fixture
def mock_medicine():
    med = Mock()
    med.name = "Paracetamol"
    med.price = 10.0
    med.toJson.return_value = {"name": "Paracetamol", "price": 10.0}
    return med


@pytest.fixture
def cart_setup(mock_medicine):
    sales = Mock()
    inventory = Mock()
    cart = Cart(sales, inventory)
    return cart, mock_medicine, sales, inventory


def test_init_valid(cart_setup):
    cart, _, _, _ = cart_setup
    assert isinstance(cart.cart, dict)


def test_add_item_new(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 2)
    assert cart.cart[med] == 2


def test_add_item_existing(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 1)
    cart.add_item(med, 2)
    assert cart.cart[med] == 3


def test_add_item_invalid(cart_setup):
    cart, *_ = cart_setup
    with pytest.raises(ValueError):
        cart.add_item(None, 1)
    with pytest.raises(ValueError):
        cart.add_item(Mock(), 0)


def test_remove_item(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 3)
    cart.remove_item(med, 2)
    assert cart.cart[med] == 1


def test_remove_item_full(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 3)
    cart.remove_item(med, 3)
    assert med not in cart.cart


def test_remove_item_excess(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 1)
    with pytest.raises(ValueError, match="Not enough quantity to remove"):
        cart.remove_item(med, 2)


def test_remove_item_missing(cart_setup):
    cart, med, *_ = cart_setup
    with pytest.raises(ValueError, match="Medicine not found in cart"):
        cart.remove_item(med, 1)


def test_calculate_total(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 3)
    assert cart.calculate_total() == 30.0


def test_generate_receipt_json(cart_setup):
    cart, med, sales, inventory = cart_setup
    cart.add_item(med, 2)

    inventory.get_quantity.return_value = 5
    receipt = cart.generate_reciept_json()

    assert receipt["total"] == 20.0
    assert receipt["items"][0]["name"] == "Paracetamol"
    inventory.remove_medicine.assert_called_once()
    sales.add_sale.assert_called_once_with(cart)


def test_generate_receipt_insufficient_inventory(cart_setup):
    cart, med, _, inventory = cart_setup
    cart.add_item(med, 2)

    inventory.get_quantity.return_value = 1
    with pytest.raises(ValueError, match="Not enough Paracetamol in inventory"):
        cart.generate_reciept_json()


def test_get_cart(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 1)
    assert cart.get_cart()[med] == 1


def test_get_cart_json(cart_setup):
    cart, med, *_ = cart_setup
    cart.add_item(med, 2)
    result = cart.get_cart_json()
    assert result[0]["name"] == "Paracetamol"
    assert result[0]["quantity"] == 2
    assert result[0]["total_price"] == 20.0
