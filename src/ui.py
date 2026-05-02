"""
User Interface for Warehouse Management System Tier 2
Provides console-based interface for warehouse operations with FIFO batch tracking
"""

from datetime import datetime
from .warehouse import Warehouse
from .item import Item

class UserInterface:
    """
    Console-based user interface for the WMS Tier 2
    """
    
    def __init__(self):
        """Initialize the user interface"""
        self.warehouse = Warehouse()
        self.running = True
        
    def start(self):
        """Start the main program loop"""
        print("\n" + "="*60)
        print("WAREHOUSE MANAGEMENT SYSTEM - TIER 2 (FIFO Batches)")
        print("="*60)
        
        # Setup demo data
        self._setup_demo_data()
        
        while self.running:
            self._show_main_menu()
            
    def _setup_demo_data(self):
        """Add demo items with multiple batches for FIFO demonstration"""
        print("\nSetting up demo inventory with FIFO batches...")
        
        # Create items
        items = [
            Item("ITM001", "Widget A", "Standard widget", 10.50),
            Item("ITM002", "Widget B", "Premium widget", 25.00),
            Item("ITM003", "Gadget X", "Electronic gadget", 50.00),
        ]
        
        # Add multiple batches with different dates and suppliers
        from datetime import timedelta
        
        # Widget A - 3 batches
        self.warehouse.add_item(items[0], 100, "Supplier Alpha", 
                               datetime.now() - timedelta(days=10), 9.50)
        self.warehouse.add_item(items[0], 50, "Supplier Beta", 
                               datetime.now() - timedelta(days=5), 10.00)
        self.warehouse.add_item(items[0], 75, "Supplier Alpha", 
                               datetime.now() - timedelta(days=2), 11.00)
        
        # Widget B - 2 batches
        self.warehouse.add_item(items[1], 60, "Supplier Gamma", 
                               datetime.now() - timedelta(days=15), 24.00)
        self.warehouse.add_item(items[1], 40, "Supplier Alpha", 
                               datetime.now() - timedelta(days=3), 26.00)
        
        # Gadget X - 1 batch
        self.warehouse.add_item(items[2], 30, "Supplier Delta", 
                               datetime.now() - timedelta(days=7), 50.00)
        
        print("Demo data ready! Notice different batch dates for FIFO demonstration.")
            
    def _show_main_menu(self):
        """Display the main menu and handle user input"""
        print("\n" + "-"*40)
        print("MAIN MENU")
        print("-"*40)
        print("1. View Stock Summary")
        print("2. View Item Details with Batches")
        print("3. Add New Batch (Receive Items)")
        print("4. Remove Items (FIFO - Oldest First)")
        print("5. View FIFO Queue for Item")
        print("6. View Transaction History")
        print("7. Track Specific Batch")
        print("8. Exit")
        print("-"*40)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            self._view_stock_summary()
        elif choice == "2":
            self._view_item_details()
        elif choice == "3":
            self._add_batch()
        elif choice == "4":
            self._remove_items()
        elif choice == "5":
            self._view_fifo_queue()
        elif choice == "6":
            self._view_transaction_history()
        elif choice == "7":
            self._track_batch()
        elif choice == "8":
            self._exit_program()
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
            
    def _view_stock_summary(self):
        """Display the stock summary with batch information"""
        print(self.warehouse.get_stock_summary())
        
    def _view_item_details(self):
        """View details of a specific item with batch breakdown"""
        item_id = input("Enter item ID to view: ").strip().upper()
        
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        stock_info = self.warehouse.check_stock(item_id)
        
        if "error" in stock_info:
            print(f"\n{stock_info['error']}")
            return
            
        item = stock_info["item"]
        
        print(f"\n{'='*50}")
        print(f"ITEM DETAILS WITH BATCHES")
        print(f"{'='*50}")
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print(f"Total Quantity: {stock_info['total_quantity']} units")
        print(f"Total Value: ${stock_info['total_value']:.2f}")
        print(f"Number of Batches: {stock_info['batch_count']}")
        
        if stock_info['batches']:
            print(f"\nBATCH BREAKDOWN (FIFO Order):")
            print(f"{'ID':<12} {'Received':<20} {'Supplier':<15} {'Qty':<8} {'Price':<10} {'Value':<10}")
            print(f"{'-'*75}")
            
            for batch in stock_info['batches']:
                print(f"{batch['batch_id']:<12} "
                      f"{batch['received_date']:<20} "
                      f"{batch['supplier']:<15} "
                      f"{batch['quantity']:<8} "
                      f"${batch['unit_price']:<9.2f} "
                      f"${batch['total_value']:<9.2f}")
        
        print(f"{'='*50}")
        
    def _add_batch(self):
        """Add a new batch of items to the warehouse"""
        print("\nADD NEW BATCH (RECEIVE ITEMS)")
        print("-"*30)
        
        # First, show existing items
        stock = self.warehouse.check_stock()
        if stock:
            print("\nExisting items in warehouse:")
            for item_id, data in stock.items():
                print(f"  {item_id}: {data['item']['name']}")
        
        item_id = input("\nEnter item ID (new or existing): ").strip().upper()
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        # Check if item exists
        existing = self.warehouse.get_item_info(item_id)
        
        if existing:
            print(f"Adding to existing item: {existing['item']['name']}")
            item = Item(
                item_id, 
                existing['item']['name'],
                existing['item']['description'],
                existing['item']['unit_price']
            )
        else:
            # Create new item
            name = input("Enter item name: ").strip()
            if not name:
                print("Error: Item name cannot be empty")
                return
                
            description = input("Enter description (optional): ").strip()
            
            try:
                price = float(input("Enter default unit price: $"))
            except ValueError:
                print("Error: Invalid price")
                return
                
            item = Item(item_id, name, description, price)
            
        # Batch details
        supplier = input("Enter supplier name: ").strip()
        if not supplier:
            supplier = "Unknown"
            
        try:
            quantity = int(input("Enter batch quantity: "))
        except ValueError:
            print("Error: Invalid quantity")
            return
            
        batch_price = input(f"Enter batch unit price (press Enter for ${item.unit_price:.2f}): $").strip()
        if batch_price:
            try:
                unit_price = float(batch_price)
            except ValueError:
                print("Error: Invalid price, using default")
                unit_price = item.unit_price
        else:
            unit_price = item.unit_price
            
        # Optional: custom received date
        use_custom_date = input("Enter custom received date? (y/n): ").strip().lower()
        received_date = None
        if use_custom_date == 'y':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                received_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format, using current date")
                
        self.warehouse.add_item(item, quantity, supplier, received_date, unit_price)
        
    def _remove_items(self):
        """Remove items using FIFO logic"""
        print("\nREMOVE ITEMS (FIFO - OLDEST BATCHES FIRST)")
        print("-"*30)
        
        # Show available items
        stock = self.warehouse.check_stock()
        if not stock:
            print("Warehouse is empty. Nothing to remove.")
            return
            
        print("Available items:")
        for item_id, data in stock.items():
            print(f"  {item_id}: {data['item']['name']} (Total: {data['total_quantity']} units)")
            
        item_id = input("\nEnter item ID to remove: ").strip().upper()
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        # Show FIFO queue before removal
        fifo_queue = self.warehouse.get_fifo_queue(item_id)
        if fifo_queue:
            print(f"\nFIFO Queue (will be removed in this order):")
            for i, batch in enumerate(fifo_queue, 1):
                print(f"  {i}. {batch.batch_id} - {batch.quantity} units "
                      f"(received: {batch.received_date.strftime('%Y-%m-%d')})")
            
        try:
            quantity = int(input("\nEnter quantity to remove: "))
        except ValueError:
            print("Error: Invalid quantity")
            return
            
        print(f"\nRemoving {quantity} units using FIFO...")
        self.warehouse.remove_item(item_id, quantity)
        
    def _view_fifo_queue(self):
        """View the FIFO queue for a specific item"""
        item_id = input("Enter item ID to view FIFO queue: ").strip().upper()
        
        if not item_id:
            print("Error: Item ID cannot be empty")
            return
            
        fifo_queue = self.warehouse.get_fifo_queue(item_id)
        
        if not fifo_queue:
            print(f"No batches found for item {item_id}")
            return
            
        print(f"\nFIFO QUEUE - {item_id}")
        print(f"(Oldest batches will be used first)")
        print(f"{'='*60}")
        print(f"{'Order':<8} {'Batch ID':<12} {'Received':<20} {'Supplier':<15} {'Qty':<8}")
        print(f"{'-'*60}")
        
        for i, batch in enumerate(fifo_queue, 1):
            print(f"{i:<8} {batch.batch_id:<12} "
                  f"{batch.received_date.strftime('%Y-%m-%d %H:%M'):<20} "
                  f"{batch.supplier:<15} "
                  f"{batch.quantity:<8}")
                  
    def _view_transaction_history(self):
        """View recent transactions with batch details"""
        transactions = self.warehouse.get_transaction_history()
        
        if not transactions:
            print("\nNo transactions recorded yet.")
            return
            
        print(f"\n{'='*80}")
        print(f"TRANSACTION HISTORY (Last 20 transactions)")
        print(f"{'='*80}")
        
        for trans in transactions[-20:]:
            print(f"\n[{trans['timestamp']}] {trans['action']}")
            print(f"  Item: {trans['item_name']} (ID: {trans['item_id']})")
            print(f"  Quantity: {trans['quantity']}")
            
            if trans['action'] == 'ADD':
                print(f"  Batch: {trans.get('batch_id', 'N/A')}")
                print(f"  Supplier: {trans.get('supplier', 'N/A')}")
            elif trans['action'] == 'REMOVE':
                batch_details = trans.get('batch_details', [])
                if batch_details:
                    print(f"  Batches used:")
                    for detail in batch_details:
                        status = "DEPLETED" if detail['depleted'] else "partial"
                        print(f"    - {detail['batch_id']}: {detail['quantity']} units ({status})")
                        
        print(f"{'='*80}")
        
    def _track_batch(self):
        """Track a specific batch by its ID"""
        batch_id = input("Enter batch ID to track: ").strip().upper()
        
        if not batch_id:
            print("Error: Batch ID cannot be empty")
            return
            
        batch_details = self.warehouse.get_batch_details(batch_id)
        
        if not batch_details:
            print(f"Batch {batch_id} not found in warehouse")
            return
            
        item = batch_details["item"]
        batch = batch_details["batch"]
        
        print(f"\n{'='*50}")
        print(f"BATCH TRACKING")
        print(f"{'='*50}")
        print(f"Batch ID: {batch['batch_id']}")
        print(f"Item: {item['name']} (ID: {item['id']})")
        print(f"Received: {batch['received_date']}")
        print(f"Supplier: {batch['supplier']}")
        print(f"Remaining Quantity: {batch['quantity']} units")
        print(f"Unit Price: ${batch['unit_price']:.2f}")
        print(f"Current Value: ${batch['total_value']:.2f}")
        print(f"{'='*50}")
        
    def _exit_program(self):
        """Exit the program"""
        print("\nThank you for using Warehouse Management System!")
        print("Final stock summary:")
        print(self.warehouse.get_stock_summary())
        self.running = False