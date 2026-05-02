"""
User Interface for Warehouse Management System Tier 3
Individual item tracking with serial numbers
"""

from .tracked_warehouse import TrackedWarehouse
from .item import Item


class TrackedUI:
    """
    Console UI for tracked warehouse (Tier 3)
    """
    
    def __init__(self):
        """Initialize the UI"""
        self.warehouse = TrackedWarehouse("Tracked Warehouse")
        self.running = True
        
    def start(self):
        """Start the program"""
        print("\n" + "="*60)
        print("WAREHOUSE MANAGEMENT SYSTEM - TIER 3")
        print("Individual Item Tracking")
        print("="*60)
        
        self._setup_demo()
        
        while self.running:
            self._show_menu()
            
    def _setup_demo(self):
        """Add demo items"""
        print("\nSetting up tracked inventory...")
        
        items_data = [
            ("ITM001", "Widget A", "Standard widget", 10.50),
            ("ITM001", "Widget A", "Standard widget", 10.50),
            ("ITM001", "Widget A", "Standard widget", 10.50),
            ("ITM002", "Widget B", "Premium widget", 25.00),
            ("ITM002", "Widget B", "Premium widget", 25.00),
            ("ITM003", "Gadget X", "Electronic gadget", 50.00),
        ]
        
        suppliers = ["Supplier Alpha", "Supplier Beta", "Supplier Gamma",
                    "Supplier Alpha", "Supplier Beta", "Supplier Delta"]
        locations = ["Shelf A1", "Shelf A2", "Shelf B1", "Shelf B2", "Shelf C1", "Shelf C2"]
        
        for i, (item_id, name, desc, price) in enumerate(items_data):
            item = Item(item_id, name, desc, price)
            self.warehouse.receive_item(item, suppliers[i], locations[i])
            
        print(f"Demo ready: {len(self.warehouse._items)} items tracked")
        
    def _show_menu(self):
        """Main menu"""
        print("\n" + "-"*40)
        print("TIER 3 - INDIVIDUAL ITEM TRACKING")
        print("-"*40)
        print("1. View Stock Summary")
        print("2. Receive New Item")
        print("3. Ship Item to Customer")
        print("4. Track Item (by Serial Number)")
        print("5. Move Item Location")
        print("6. Search Items")
        print("7. View Transaction History")
        print("8. Exit")
        print("-"*40)
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice == "1":
            print(self.warehouse.get_stock_summary())
        elif choice == "2":
            self._receive_item()
        elif choice == "3":
            self._ship_item()
        elif choice == "4":
            self._track_item()
        elif choice == "5":
            self._move_item()
        elif choice == "6":
            self._search_items()
        elif choice == "7":
            self._view_transactions()
        elif choice == "8":
            self._exit()
        else:
            print("Invalid choice")
            
    def _receive_item(self):
        """Receive a new item"""
        print("\nRECEIVE NEW ITEM")
        print("-"*30)
        
        item_id = input("Enter product ID: ").strip().upper()
        if not item_id:
            print("Error: ID required")
            return
            
        name = input("Enter product name: ").strip()
        if not name:
            print("Error: Name required")
            return
            
        description = input("Description (optional): ").strip()
        
        try:
            price = float(input("Unit price: $"))
        except ValueError:
            print("Error: Invalid price")
            return
            
        supplier = input("Supplier: ").strip() or "Unknown"
        location = input("Storage location: ").strip() or "Warehouse A"
        
        serial = input("Custom serial (press Enter for auto): ").strip()
        if not serial:
            serial = None
            
        item = Item(item_id, name, description, price)
        self.warehouse.receive_item(item, supplier, location, serial)
        
    def _ship_item(self):
        """Ship an item"""
        print("\nSHIP ITEM TO CUSTOMER")
        print("-"*30)
        
        in_stock = self.warehouse.get_all_items("in_stock")
        if not in_stock:
            print("No items in stock")
            return
            
        print("Items in stock:")
        for item in in_stock:
            print(f"  {item.serial_number}: {item.name} ({item.location})")
            
        serial = input("\nEnter serial number to ship: ").strip().upper()
        if not serial:
            return
            
        customer = input("Customer name: ").strip()
        if not customer:
            print("Error: Customer required")
            return
            
        self.warehouse.ship_item(serial, customer)
        
    def _track_item(self):
        """View item history"""
        serial = input("Enter serial number: ").strip().upper()
        if not serial:
            return
            
        history = self.warehouse.get_item_history(serial)
        if history:
            print(history)
        else:
            print(f"Item {serial} not found")
            
    def _move_item(self):
        """Move item location"""
        serial = input("Enter serial number: ").strip().upper()
        if not serial:
            return
            
        item = self.warehouse.get_item(serial)
        if not item:
            print(f"Item {serial} not found")
            return
            
        print(f"Current location: {item.location}")
        new_location = input("New location: ").strip()
        if new_location:
            self.warehouse.move_item(serial, new_location)
            
    def _search_items(self):
        """Search for items"""
        query = input("Search (name/serial/location): ").strip()
        if not query:
            return
            
        results = self.warehouse.search_items(query)
        if results:
            print(f"\nFound {len(results)} items:")
            for item in results:
                print(f"  {item.get_summary()}")
        else:
            print("No items found")
            
    def _view_transactions(self):
        """View recent transactions"""
        transactions = self.warehouse.get_transaction_history()
        if not transactions:
            print("No transactions yet")
            return
            
        print(f"\n{'='*60}")
        print("RECENT TRANSACTIONS")
        print(f"{'='*60}")
        for t in transactions:
            print(f"[{t['timestamp']}] {t['action']}: {t['serial_number']} - {t['name']}")
            
    def _exit(self):
        """Exit"""
        print("\n" + self.warehouse.get_stock_summary())
        print("Goodbye!")
        self.running = False