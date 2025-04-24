import pytest
from ..batch import Batch, BatchList


@pytest.fixture
def sample_batch():
    return Batch("B123", "2025-12-31")


@pytest.fixture
def batch_list_with_one(sample_batch):
    bl = BatchList()
    bl.add_batch(sample_batch)
    return bl

def test_batch_creation(sample_batch):
    batch = sample_batch
    assert batch.batch_number == "B123"
    assert batch.expiry_date == "2025-12-31"


def test_add_batch_valid(sample_batch):
    bl = BatchList()
    bl.add_batch(sample_batch)
    assert sample_batch in bl.get_batches()


def test_add_batch_invalid():
    bl = BatchList()
    with pytest.raises(ValueError, match="Batch cannot be None"):
        bl.add_batch(None)


def test_remove_existing_batch(batch_list_with_one, sample_batch):
    batch_list_with_one.remove_batch("B123")
    assert sample_batch not in batch_list_with_one.get_batches()


def test_remove_non_existing_batch(batch_list_with_one):
    original_batches = batch_list_with_one.get_batches().copy()
    batch_list_with_one.remove_batch("NON_EXISTENT")
    assert batch_list_with_one.get_batches() == original_batches


def test_get_batches_returns_list(sample_batch):
    bl = BatchList()
    bl.add_batch(sample_batch)
    assert isinstance(bl.get_batches(), list)
    assert bl.get_batches()[0] == sample_batch


def test_find_existing_batch(batch_list_with_one, sample_batch):
    found = batch_list_with_one.find_batch("B123")
    assert found == sample_batch


def test_find_non_existing_batch(batch_list_with_one):
    assert batch_list_with_one.find_batch("B999") is None


def test_to_json_returns_correct_format(sample_batch):
    bl = BatchList()
    bl.add_batch(sample_batch)
    json_data = bl.toJson()
    assert isinstance(json_data, list)
    assert json_data[0] == {
        "batch_number": "B123",
        "expiry_date": "2025-12-31"
    }
