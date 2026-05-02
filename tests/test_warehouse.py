
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.item import Item
from src.warehouse import Warehouse

def test_item_creation():
    """Test item object creation"""
    item = Item("TEST001", "Test Item", "A test item", 10.00)
    assert item.item_id == "TEST001"
    assert item.name == "Test Item"
    assert item.unit_price == 10.00
    print("✓ Item creation test passed")

def test_add_item():
    """Test adding items to warehouse"""
    warehouse = Warehouse("Test Warehouse")
    item = Item("TEST001", "Test Item", "Test", 10.00)

    assert warehouse.add_item(item, 50) == True
    assert warehouse.add_item(item, 30) == True
    stock = warehouse.check_stock("TEST001")
    assert stock["quantity"] == 80

    assert warehouse.add_item(item, -10) == False
    
    print("✓ Add item test passed")

def test_remove_item():
    """Test removing items from warehouse"""
    warehouse = Warehouse("Test Warehouse")
    item = Item("TEST001", "Test Item", "Test", 10.00)
    warehouse.add_item(item, 100)

    assert warehouse.remove_item("TEST001", 30) == True
    stock = warehouse.check_stock("TEST001")
    assert stock["quantity"] == 70

    assert warehouse.remove_item("NONEXIST", 10) == False

    assert warehouse.remove_item("TEST001", 100) == False
    
    print("✓ Remove item test passed")

def test_stock_check():
    """Test checking stock levels"""
    warehouse = Warehouse("Test Warehouse")
    item1 = Item("TEST001", "Item 1", "Test", 10.00)
    item2 = Item("TEST002", "Item 2", "Test", 20.00)
    
    warehouse.add_item(item1, 50)
    warehouse.add_item(item2, 30)

    all_stock = warehouse.check_stock()
    assert len(all_stock) == 2
    assert "TEST001" in all_stock
    assert "TEST002" in all_stock

    stock = warehouse.check_stock("TEST001")
    assert stock["quantity"] == 50
    assert stock["item"]["name"] == "Item 1"
    
    print("✓ Stock check test passed")

def test_transaction_log():
    """Test transaction logging"""
    warehouse = Warehouse("Test Warehouse")
    item = Item("TEST001", "Test Item", "Test", 10.00)
    
    warehouse.add_item(item, 50)
    warehouse.remove_item("TEST001", 20)
    
    transactions = warehouse.get_transaction_history()
    assert len(transactions) == 2
    assert transactions[0]["action"] == "ADD"
    assert transactions[1]["action"] == "REMOVE"
    
    print("✓ Transaction log test passed")

def run_all_tests():
    """Run all test cases"""
    print("\nRunning Tier 1 WMS Tests...")
    print("-" * 40)
    
    try:
        test_item_creation()
        test_add_item()
        test_remove_item()
        test_stock_check()
        test_transaction_log()
        
        print("-" * 40)
        print("All tests passed successfully! ✓")
        return True
    except AssertionError as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()