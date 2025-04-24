import pytest
from unittest.mock import Mock
from ..inventory import Inventory


@pytest.fixture
def mock_medicine():
    med = Mock()
    med.identifier = "med001"
    med.price = 10.0
    med.batch.expiry_date = "2024-01-01"
    med.toJson.return_value = {"identifier": "med001", "price": 10.0}
    return med


def test_inventory_init_valid(mock_medicine):
    inv = Inventory([mock_medicine], [5])
    assert inv.get_quantity(mock_medicine) == 5


def test_inventory_init_mismatch_length(mock_medicine):
    with pytest.raises(ValueError):
        Inventory([mock_medicine], [1, 2])


def test_add_medicine(mock_medicine):
    inv = Inventory()
    inv.add_medicine(mock_medicine, 3)
    assert inv.get_quantity(mock_medicine) == 3


def test_add_medicine_existing(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    inv.add_medicine(mock_medicine, 3)
    assert inv.get_quantity(mock_medicine) == 5


def test_add_invalid_medicine():
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.add_medicine(None, 1)
    with pytest.raises(ValueError):
        inv.add_medicine(Mock(), 0)


def test_remove_medicine(mock_medicine):
    inv = Inventory([mock_medicine], [5])
    inv.remove_medicine(mock_medicine, 3)
    assert inv.get_quantity(mock_medicine) == 2


def test_remove_medicine_to_zero(mock_medicine):
    inv = Inventory([mock_medicine], [3])
    inv.remove_medicine(mock_medicine, 3)
    assert mock_medicine not in inv.inventory


def test_remove_medicine_excess(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    with pytest.raises(ValueError, match="Not enough quantity"):
        inv.remove_medicine(mock_medicine, 5)


def test_remove_medicine_not_found(mock_medicine):
    inv = Inventory()
    with pytest.raises(ValueError, match="Medicine not found"):
        inv.remove_medicine(mock_medicine, 1)


def test_get_quantity_not_found(mock_medicine):
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.get_quantity(mock_medicine)


def test_queue_order(mock_medicine):
    inv = Inventory()
    inv.queue_order(mock_medicine, 5)
    mock_medicine.send_to_vendor.assert_called_once_with(5)


def test_queue_order_invalid():
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.queue_order(None, 5)
    with pytest.raises(ValueError):
        inv.queue_order(Mock(), 0)


def test_search_medicine(mock_medicine):
    inv = Inventory([mock_medicine], [1])
    found = inv.search_medicine("med001")
    assert found == mock_medicine


def test_search_medicine_not_found(mock_medicine):
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.search_medicine("xyz")


def test_get_medicines(mock_medicine):
    inv = Inventory([mock_medicine], [3])
    meds = inv.get_medicines()
    assert meds == [mock_medicine]


def test_get_stock_valuation(mock_medicine):
    inv = Inventory([mock_medicine], [4])
    assert inv.get_stock_valuation() == 40.0


def test_get_threshold_alerts(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    alerts = inv.get_threshold_alerts(3)
    assert (mock_medicine, 2) in alerts


def test_threshold_alerts_invalid_threshold(mock_medicine):
    inv = Inventory([mock_medicine], [1])
    with pytest.raises(ValueError):
        inv.get_threshold_alerts(0)


def test_track_batch_expiry(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    expired = inv.track_batch_expiry("2025-01-01")
    assert (mock_medicine, "2024-01-01") in expired


def test_track_batch_expiry_invalid_date(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    with pytest.raises(ValueError):
        inv.track_batch_expiry("bad-date")


def test_toJson(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    json_data = inv.toJson()
    assert json_data[0]["medicine"]["identifier"] == "med001"
    assert json_data[0]["quantity"] == 2


def test_threshold_toJson(mock_medicine):
    inv = Inventory([mock_medicine], [1])
    result = inv.threshold_toJson(2)
    assert result[0]["quantity"] == 1


def test_threshold_toJson_invalid():
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.threshold_toJson(0)


def test_expiry_toJson(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    data = inv.expiry_toJson("2025-01-01")
    assert data[0]["expiry_date"] == "2024-01-01"


def test_expiry_toJson_invalid_date(mock_medicine):
    inv = Inventory([mock_medicine], [2])
    with pytest.raises(ValueError):
        inv.expiry_toJson("wrong-format")
