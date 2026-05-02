"""
Tests for Warehouse Management System Tier 2 - FIFO Batches
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from src.item import Item
from src.batch import Batch
from src.warehouse import Warehouse

def test_batch_creation():
    """Test batch object creation"""
    batch = Batch(
        received_date=datetime.now(),
        supplier="Test Supplier",
        quantity=100,
        unit_price=10.50
    )
    
    assert batch.quantity == 100
    assert batch.supplier == "Test Supplier"
    assert batch.unit_price == 10.50
    assert batch.get_value() == 1050.0
    print("✓ Batch creation test passed")

def test_batch_quantity_operations():
    """Test adding and removing quantities from batch"""
    batch = Batch(quantity=50, unit_price=10.0)
    
    # Test removal
    removed, depleted = batch.remove_quantity(20)
    assert removed == 20
    assert not depleted
    assert batch.quantity == 30
    
    # Test depletion
    removed, depleted = batch.remove_quantity(30)
    assert removed == 30
    assert depleted
    assert batch.quantity == 0
    
    # Test adding
    batch.add_quantity(25)
    assert batch.quantity == 25
    
    print("✓ Batch quantity operations test passed")

def test_fifo_addition():
    """Test adding items with FIFO batch tracking"""
    warehouse = Warehouse("Test FIFO Warehouse")
    item = Item("TEST001", "FIFO Item", "Test", 10.00)
    
    # Add batches with different dates
    date1 = datetime.now() - timedelta(days=10)
    date2 = datetime.now() - timedelta(days=5)
    date3 = datetime.now() - timedelta(days=1)
    
    warehouse.add_item(item, 100, "Supplier A", date1, 9.50)
    warehouse.add_item(item, 50, "Supplier B", date2, 10.00)
    warehouse.add_item(item, 75, "Supplier A", date3, 10.50)
    
    # Check stock
    stock = warehouse.check_stock("TEST001")
    assert stock["total_quantity"] == 225
    assert stock["batch_count"] == 3
    
    print("✓ FIFO addition test passed")

def test_fifo_removal():
    """Test FIFO removal logic"""
    warehouse = Warehouse("Test FIFO Warehouse")
    item = Item("TEST001", "FIFO Item", "Test", 10.00)
    
    # Add batches with known dates
    date1 = datetime.now() - timedelta(days=10)
    date2 = datetime.now() - timedelta(days=5)
    date3 = datetime.now() - timedelta(days=1)
    
    warehouse.add_item(item, 100, "Supplier A", date1, 9.50)
    warehouse.add_item(item, 50, "Supplier B", date2, 10.00)
    warehouse.add_item(item, 75, "Supplier A", date3, 10.50)
    
    # Remove 120 units - should deplete oldest batch and take 20 from second
    warehouse.remove_item("TEST001", 120)
    
    stock = warehouse.check_stock("TEST001")
    assert stock["total_quantity"] == 105  # 225 - 120
    assert stock["batch_count"] == 2  # Oldest batch depleted
    
    # Check remaining batches are the newer ones
    batches = warehouse.get_fifo_queue("TEST001")
    assert len(batches) == 2
    assert batches[0].quantity == 30  # Second batch had 20 removed
    assert batches[1].quantity == 75  # Third batch untouched
    
    print("✓ FIFO removal test passed")

def test_fifo_ordering():
    """Test that FIFO queue returns batches in correct order"""
    warehouse = Warehouse("Test FIFO Warehouse")
    item = Item("TEST001", "FIFO Item", "Test", 10.00)
    
    # Add batches in reverse order
    date1 = datetime.now() - timedelta(days=10)
    date2 = datetime.now() - timedelta(days=5)
    date3 = datetime.now() - timedelta(days=1)
    
    warehouse.add_item(item, 100, "Supplier A", date2)  # Middle date
    warehouse.add_item(item, 50, "Supplier B", date1)   # Oldest date
    warehouse.add_item(item, 75, "Supplier A", date3)   # Newest date
    
    # Get FIFO queue
    fifo_queue = warehouse.get_fifo_queue("TEST001")
    
    # Should be ordered oldest first
    assert len(fifo_queue) == 3
    assert fifo_queue[0].received_date == date1  # Oldest
    assert fifo_queue[1].received_date == date2  # Middle
    assert fifo_queue[2].received_date == date3  # Newest
    
    print("✓ FIFO ordering test passed")

def test_batch_tracking():
    """Test tracking specific batches"""
    warehouse = Warehouse("Test FIFO Warehouse")
    item = Item("TEST001", "FIFO Item", "Test", 10.00)
    
    warehouse.add_item(item, 100, "Supplier A")
    
    stock = warehouse.check_stock("TEST001")
    batch_id = stock["batches"][0]["batch_id"]
    
    # Track the batch
    batch_details = warehouse.get_batch_details(batch_id)
    assert batch_details is not None
    assert batch_details["item"]["name"] == "FIFO Item"
    assert batch_details["batch"]["quantity"] == 100
    
    print("✓ Batch tracking test passed")

def run_all_tests():
    """Run all Tier 2 test cases"""
    print("\nRunning Tier 2 WMS Tests (FIFO Batches)...")
    print("-" * 50)
    
    try:
        test_batch_creation()
        test_batch_quantity_operations()
        test_fifo_addition()
        test_fifo_removal()
        test_fifo_ordering()
        test_batch_tracking()
        
        print("-" * 50)
        print("All Tier 2 tests passed successfully! ✓")
        return True
    except AssertionError as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()