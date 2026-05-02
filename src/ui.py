"""
User Interface for Warehouse Management System Tier 1
Provides console-based interface for warehouse operations
"""

from .warehouse import Warehouse
from .item import Item

class UserInterface:
    """
    Console-based user interface for the WMS
    """
    
    def __init__(self):
        """Initialize the user interface"""
        self.warehouse = Warehouse()
        self.running = True
        
    def start(self):
        """Start the main program loop"""
        print("\n" + "="*60)
        print("WAREHOUSE MANAGEMENT SYSTEM - TIER 1 (Bulk Storage)")
        print("="*60)
        
        # Setup demo data (optional)
        self._setup_demo_data()
        
        while self.running:
            self._show_main_menu()
            
    def _setup_demo_data(self):
        """Add some demo items for testing"""
        demo_items = [
            Item("ITM001", "Widget A", "Standard widget", 10.50),
            Item("ITM002", "Widget B", "Premium widget", 25.00),
            Item("ITM003", "Gadget X", "Electronic gadget", 50.00),
            Item("ITM004", "Bolt M10", "10mm steel bolt", 0.50),
            Item("ITM005", "Cable USB", "USB Type-C cable", 5.00)
        ]
        
        print("\nSetting up demo inventory...")
        for item in demo_items:
            import random
            qty = random.randint(50, 200)
            self.warehouse.add_item(item, qty)
            
    def _show_main_menu(self):
        """Display the main menu and handle user input"""
        print("\n" + "-"*40)
        print("MAIN MENU")
        print("-"*40)
        print("1. View Stock Summary")
        print("2. View Item Details")
        print("3. Add Items to Stock")
        print("4. Remove Items from Stock")
        print("5. View Transaction History")
        print("6. Exit")
        print("-"*40)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            self._view_stock_summary()
        elif choice == "2":
            self._view_item_details()
        elif choice == "3":
            self._add_items()
        elif choice == "4":
            self._remove_items()
        elif choice == "5":
            self._view_transaction_history()
        elif choice == "6":
            self._exit_program()
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            
    def _view_stock_summary(self):
        """Display the stock summary"""
        print(self.warehouse.get_stock_summary())
        
    def _view_item_details(self):
        """View details of a specific item"""
        item_id = input("Enter item ID to view: ").strip().upper()
        
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        stock_info = self.warehouse.check_stock(item_id)
        
        if "error" in stock_info:
            print(f"\n{stock_info['error']}")
            return
            
        item = stock_info["item"]
        qty = stock_info["quantity"]
        
        print(f"\n{'='*40}")
        print(f"ITEM DETAILS")
        print(f"{'='*40}")
        print(f"ID:          {item['id']}")
        print(f"Name:        {item['name']}")
        print(f"Description: {item['description']}")
        print(f"Unit Price:  ${item['unit_price']:.2f}")
        print(f"Quantity:    {qty} units")
        print(f"Total Value: ${qty * item['unit_price']:.2f}")
        print(f"{'='*40}")
        
    def _add_items(self):
        """Add new or existing items to the warehouse"""
        print("\nADD ITEMS TO WAREHOUSE")
        print("-"*30)
        
        item_id = input("Enter item ID: ").strip().upper()
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        # Check if item exists
        existing = self.warehouse.get_item_info(item_id)
        
        if existing:
            print(f"Item exists: {existing['item']['name']}")
            print(f"Current quantity: {existing['quantity']}")
            try:
                quantity = int(input("Enter quantity to add: "))
                self.warehouse.add_item(existing['item'], quantity)
            except ValueError:
                print("Error: Invalid quantity")
        else:
            # Create new item
            name = input("Enter item name: ").strip()
            if not name:
                print("Error: Item name cannot be empty")
                return
                
            description = input("Enter description (optional): ").strip()
            
            try:
                price = float(input("Enter unit price: $"))
            except ValueError:
                print("Error: Invalid price")
                return
                
            try:
                quantity = int(input("Enter initial quantity: "))
            except ValueError:
                print("Error: Invalid quantity")
                return
                
            new_item = Item(item_id, name, description, price)
            self.warehouse.add_item(new_item, quantity)
            
    def _remove_items(self):
        """Remove items from the warehouse"""
        print("\nREMOVE ITEMS FROM WAREHOUSE")
        print("-"*30)
        
        # Show available items
        stock = self.warehouse.check_stock()
        if not stock:
            print("Warehouse is empty. Nothing to remove.")
            return
            
        print("Available items:")
        for item_id, data in stock.items():
            print(f"  {item_id}: {data['item']['name']} (Qty: {data['quantity']})")
            
        item_id = input("\nEnter item ID to remove: ").strip().upper()
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        try:
            quantity = int(input("Enter quantity to remove: "))
        except ValueError:
            print("Error: Invalid quantity")
            return
            
        self.warehouse.remove_item(item_id, quantity)
        
    def _view_transaction_history(self):
        """View recent transactions"""
        transactions = self.warehouse.get_transaction_history()
        
        if not transactions:
            print("\nNo transactions recorded yet.")
            return
            
        print(f"\n{'='*60}")
        print(f"TRANSACTION HISTORY (Last 20 transactions)")
        print(f"{'='*60}")
        print(f"{'Timestamp':<20} {'Action':<10} {'Item ID':<10} {'Name':<15} {'Qty':<5}")
        print(f"{'-'*60}")
        
        for trans in transactions[-20:]:  # Show last 20
            print(f"{trans['timestamp']:<20} {trans['action']:<10} "
                  f"{trans['item_id']:<10} {trans['item_name']:<15} "
                  f"{trans['quantity']:<5}")
        print(f"{'='*60}")
        
    def _exit_program(self):
        """Exit the program"""
        print("\nThank you for using Warehouse Management System!")
        print("Final stock summary:")
        print(self.warehouse.get_stock_summary())
        self.running = False