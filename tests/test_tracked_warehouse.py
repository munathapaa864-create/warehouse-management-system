"""
Tests for Warehouse Management System Tier 3 - Individual Item Tracking
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.item import Item
from src.tracked_item import TrackedItem
from src.tracked_warehouse import TrackedWarehouse


def test_tracked_item_creation():
    """Test tracked item with serial number"""
    item = TrackedItem("ITM001", "Test Item", serial_number="SN-TEST001",
                      description="Test", unit_price=10.00)
    
    assert item.serial_number == "SN-TEST001"
    assert item.status == "in_stock"
    assert item.unit_price == 10.00
    print("✓ Tracked item creation passed")


def test_auto_serial_number():
    """Test auto-generated serial numbers"""
    item1 = TrackedItem("ITM001", "Item 1")
    item2 = TrackedItem("ITM001", "Item 2")
    
    assert item1.serial_number != item2.serial_number
    assert item1.serial_number.startswith("SN-")
    print("✓ Auto serial number passed")


def test_ship_item():
    """Test shipping an item"""
    item = TrackedItem("ITM001", "Test Item")
    assert item.status == "in_stock"
    
    result = item.ship("Customer A")
    assert result == True
    assert item.status == "shipped"
    assert item.customer == "Customer A"
    print("✓ Ship item passed")


def test_receive_item():
    """Test receiving item into warehouse"""
    warehouse = TrackedWarehouse()
    item = Item("ITM001", "Widget", "Test", 10.00)
    
    serial = warehouse.receive_item(item, "Supplier A", "Shelf 1")
    assert serial is not None
    assert len(warehouse._items) == 1
    
    tracked = warehouse.get_item(serial)
    assert tracked.status == "in_stock"
    assert tracked.supplier == "Supplier A"
    print("✓ Receive item passed")


def test_ship_from_warehouse():
    """Test shipping from warehouse"""
    warehouse = TrackedWarehouse()
    item = Item("ITM001", "Widget", "Test", 10.00)
    
    serial = warehouse.receive_item(item)
    result = warehouse.ship_item(serial, "Customer B")
    
    assert result == True
    tracked = warehouse.get_item(serial)
    assert tracked.status == "shipped"
    assert tracked.customer == "Customer B"
    print("✓ Ship from warehouse passed")


def test_item_movement():
    """Test moving item location"""
    warehouse = TrackedWarehouse()
    item = Item("ITM001", "Widget", "Test", 10.00)
    
    serial = warehouse.receive_item(item, location="Shelf A")
    warehouse.move_item(serial, "Shelf B")
    
    tracked = warehouse.get_item(serial)
    assert tracked.location == "Shelf B"
    print("✓ Item movement passed")


def test_search_items():
    """Test search functionality"""
    warehouse = TrackedWarehouse()
    item1 = Item("ITM001", "Widget", "Test", 10.00)
    item2 = Item("ITM002", "Gadget", "Test", 20.00)
    
    warehouse.receive_item(item1, location="Zone A")
    warehouse.receive_item(item2, location="Zone B")
    
    results = warehouse.search_items("Widget")
    assert len(results) == 1
    
    results = warehouse.search_items("Zone")
    assert len(results) == 2
    print("✓ Search items passed")


def test_item_history():
    """Test item history tracking"""
    item = TrackedItem("ITM001", "Test Item")
    item.add_note("Test note 1")
    item.move_location("Shelf 2")
    
    info = item.get_info()
    assert len(info["notes"]) == 2
    print("✓ Item history passed")


def run_all_tests():
    """Run all Tier 3 tests"""
    print("\nRunning Tier 3 Tests (Individual Item Tracking)...")
    print("-" * 50)
    
    try:
        test_tracked_item_creation()
        test_auto_serial_number()
        test_ship_item()
        test_receive_item()
        test_ship_from_warehouse()
        test_item_movement()
        test_search_items()
        test_item_history()
        
        print("-" * 50)
        print("All Tier 3 tests passed! ✓")
        return True
    except AssertionError as e:
        print(f"Test failed: {e}")
        return False


if __name__ == "__main__":
    run_all_tests()