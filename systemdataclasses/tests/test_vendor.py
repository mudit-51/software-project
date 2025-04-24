import pytest
from unittest.mock import Mock
from ..vendor import Vendor, VendorList 


@pytest.fixture
def sample_vendor():
    inventory_mock = Mock()
    medicine_list_mock = Mock()
    return Vendor("V001", "HealthCorp", "contact@healthcorp.com", inventory_mock, medicine_list_mock)


def test_vendor_initialization_valid(sample_vendor):
    assert sample_vendor.vendor_id == "V001"
    assert sample_vendor.name == "HealthCorp"
    assert sample_vendor.contact_info == "contact@healthcorp.com"
    assert sample_vendor.orders == {}
    assert sample_vendor.orders_fulfilled == {}


@pytest.mark.parametrize("vendor_id, name, contact", [
    ("", "Name", "contact@a.com"),
    ("V002", "", "contact@a.com"),
    ("V002", "Name", ""),
])
def test_vendor_initialization_invalid(vendor_id, name, contact):
    with pytest.raises(ValueError):
        Vendor(vendor_id, name, contact, Mock(), Mock())


def test_add_order(sample_vendor):
    order = {"identifier": "MED123", "quantity": 10}
    sample_vendor.add_order(order)
    assert len(sample_vendor.orders) == 1


def test_fulfill_order_success(sample_vendor):
    order = {"identifier": "MED123", "quantity": 5}
    sample_vendor.add_order(order)
    order_id = list(sample_vendor.orders.keys())[0]

    medicine_mock = Mock()
    sample_vendor.medicine_list_obj.find_medicine.return_value = medicine_mock

    sample_vendor.fullfill_order(order_id)

    assert order_id in sample_vendor.orders_fulfilled
    assert order_id not in sample_vendor.orders
    sample_vendor.inventory_obj.add_medicine.assert_called_once_with(medicine_mock, 5)


def test_fulfill_order_invalid_id(sample_vendor):
    with pytest.raises(ValueError):
        sample_vendor.fullfill_order("invalid_id")


def test_fulfill_order_medicine_not_found(sample_vendor):
    order = {"identifier": "NOTFOUND", "quantity": 2}
    sample_vendor.add_order(order)
    order_id = list(sample_vendor.orders.keys())[0]
    sample_vendor.medicine_list_obj.find_medicine.return_value = None

    with pytest.raises(ValueError, match="Medicine not found"):
        sample_vendor.fullfill_order(order_id)


def test_reject_order(sample_vendor):
    order = {"identifier": "MED321", "quantity": 3}
    sample_vendor.add_order(order)
    order_id = list(sample_vendor.orders.keys())[0]
    sample_vendor.reject_order(order_id)
    assert order_id not in sample_vendor.orders


def test_vendor_str(sample_vendor):
    assert str(sample_vendor) == "Vendor ID: V001, Name: HealthCorp, Contact Info: contact@healthcorp.com"


def test_vendor_get_orders(sample_vendor):
    order = {"identifier": "XYZ", "quantity": 1}
    sample_vendor.add_order(order)
    orders = sample_vendor.get_orders()
    assert len(orders) == 1
    assert "order_id" in orders[0]


def test_vendor_get_fulfilled_orders(sample_vendor):
    order = {"identifier": "XYZ", "quantity": 1}
    sample_vendor.add_order(order)
    order_id = list(sample_vendor.orders.keys())[0]
    sample_vendor.medicine_list_obj.find_medicine.return_value = Mock()
    sample_vendor.fullfill_order(order_id)
    fulfilled = sample_vendor.get_fulfilled_orders()
    assert len(fulfilled) == 1
    assert "order_id" in fulfilled[0]


def test_vendorlist_add_and_find():
    vendor_list = VendorList()
    vendor = Mock(spec=Vendor)
    vendor.vendor_id = "V003"
    vendor_list.add_vendor(vendor)
    assert vendor_list.find_vendor("V003") == vendor


def test_vendorlist_remove():
    vendor_list = VendorList()
    vendor = Mock(spec=Vendor)
    vendor.vendor_id = "V004"
    vendor_list.add_vendor(vendor)
    vendor_list.remove_vendor("V004")
    assert vendor_list.find_vendor("V004") is None


def test_vendorlist_to_json():
    vendor = Mock(spec=Vendor)
    vendor.toJson.return_value = {"vendor_id": "V005"}
    vendor_list = VendorList()
    vendor_list.add_vendor(vendor)
    assert vendor_list.toJson() == [{"vendor_id": "V005"}]
