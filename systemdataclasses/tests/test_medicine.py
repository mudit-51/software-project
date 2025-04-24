import pytest
from unittest.mock import Mock
from ..medicine import Medicine, MedicineList


@pytest.fixture
def sample_batch():
    mock_batch = Mock()
    mock_batch.toJson.return_value = {"batch_number": "B001", "expiry_date": "2025-12-12"}
    mock_batch.expiry_date = "2025-12-12"
    return mock_batch


@pytest.fixture
def sample_vendor():
    mock_vendor = Mock()
    mock_vendor.toJson.return_value = {"vendor_id": "V001", "name": "TestVendor", "contact_info": "test@vendor.com"}
    return mock_vendor


def test_medicine_initialization_valid(sample_batch, sample_vendor):
    med = Medicine("Paracetamol", sample_batch, "2025-12-12", 50.0, sample_vendor)
    assert med.name == "Paracetamol"
    assert med.price == 50.0
    assert "paracetamol_" in med.identifier


@pytest.mark.parametrize("name, expiry, price, batch, vendor, error", [
    ("", "2025-01-01", 10, Mock(), Mock(), "Name cannot be None or empty"),
    ("Med", "", 10, Mock(), Mock(), "Expiry date cannot be None or empty"),
    ("Med", "2025-01-01", -1, Mock(), Mock(), "Price must be greater than 0"),
    ("Med", "invalid-date", 10, Mock(), Mock(), "Expiry date must be in YYYY-MM-DD format"),
    ("Med", "2025-01-01", 10, None, Mock(), "Batch cannot be None"),
    ("Med", "2025-01-01", 10, Mock(), None, "Vendor cannot be None")
])
def test_medicine_initialization_invalid(name, expiry, price, batch, vendor, error):
    with pytest.raises(ValueError, match=error):
        Medicine(name, batch, expiry, price, vendor)


def test_medicine_send_to_vendor(sample_batch, sample_vendor):
    med = Medicine("TestMed", sample_batch, "2025-01-01", 100.0, sample_vendor)
    med.send_to_vendor(3)
    sample_vendor.add_order.assert_called_once()
    assert sample_vendor.add_order.call_args[0][0]["quantity"] == 3


def test_send_to_vendor_invalid_quantity(sample_batch, sample_vendor):
    med = Medicine("TestMed", sample_batch, "2025-01-01", 100.0, sample_vendor)
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        med.send_to_vendor(0)


def test_medicine_str(sample_batch, sample_vendor):
    med = Medicine("Aspirin", sample_batch, "2025-01-01", 20.0, sample_vendor)
    result = str(med)
    assert "Aspirin" in result
    assert "2025-01-01" in result


def test_medicine_to_json(sample_batch, sample_vendor):
    med = Medicine("Ibuprofen", sample_batch, "2025-01-01", 15.0, sample_vendor)
    json_data = med.toJson()
    assert json_data["name"] == "Ibuprofen"
    assert "identifier" in json_data
    assert json_data["price"] == 15.0
    assert "batch" in json_data
    assert "vendor" in json_data


# ==== MedicineList Tests ====

@pytest.fixture
def sample_medicine(sample_batch, sample_vendor):
    return Medicine("Cough Syrup", sample_batch, "2025-01-01", 40.0, sample_vendor)


def test_add_medicine_valid(sample_medicine):
    med_list = MedicineList()
    med_list.add_medicine(sample_medicine)
    assert sample_medicine in med_list.get_medicines()


def test_add_medicine_invalid():
    med_list = MedicineList()
    with pytest.raises(ValueError):
        med_list.add_medicine(None)


def test_remove_medicine(sample_medicine):
    med_list = MedicineList()
    med_list.add_medicine(sample_medicine)
    med_list.remove_medicine(sample_medicine.identifier)
    assert sample_medicine not in med_list.get_medicines()


def test_find_medicine_exists(sample_medicine):
    med_list = MedicineList()
    med_list.add_medicine(sample_medicine)
    found = med_list.find_medicine(sample_medicine.identifier)
    assert found == sample_medicine


def test_find_medicine_not_exists():
    med_list = MedicineList()
    assert med_list.find_medicine("nonexistent_id") is None


def test_to_json(sample_medicine):
    med_list = MedicineList()
    med_list.add_medicine(sample_medicine)
    result = med_list.toJson()
    assert isinstance(result, list)
    assert result[0]["name"] == "Cough Syrup"
