"""
Tracked Warehouse class for Warehouse Management System Tier 3
Handles individual item tracking with unique serial numbers
"""

from typing import Dict, List, Optional
from datetime import datetime
from .tracked_item import TrackedItem
from .item import Item


class TrackedWarehouse:
    """
    Individual item tracking warehouse (Tier 3)
    Every item has a unique serial number
    """
    
    def __init__(self, name: str = "Tracked Warehouse", location: str = "Default Location"):
        """
        Initialize the tracked warehouse
        
        Args:
            name: Warehouse name
            location: Physical location
        """
        self.name = name
        self.location = location
        self._items: Dict[str, TrackedItem] = {}  # serial_number -> TrackedItem
        self._transaction_log: list = []
        
    def receive_item(self, item: Item, supplier: str = "Unknown",
                    location: str = "Warehouse A", serial_number: Optional[str] = None) -> Optional[str]:
        """
        Receive a single tracked item
        
        Args:
            item: Product information
            supplier: Supplier name
            location: Storage location
            serial_number: Optional custom serial number
            
        Returns:
            Serial number of the new item
        """
        tracked_item = TrackedItem(
            item_id=item.item_id,
            name=item.name,
            serial_number=serial_number,
            description=item.description,
            unit_price=item.unit_price,
            supplier=supplier,
            received_date=datetime.now(),
            status="in_stock"
        )
        tracked_item.location = location
        
        self._items[tracked_item.serial_number] = tracked_item
        
        self._log_transaction("RECEIVE", tracked_item.serial_number, 
                            item.name, supplier=supplier, location=location)
        print(f"Received: {tracked_item.serial_number} - {item.name} "
              f"from {supplier} → {location}")
        return tracked_item.serial_number
        
    def ship_item(self, serial_number: str, customer: str) -> bool:
        """
        Ship a specific item to a customer
        
        Args:
            serial_number: Item's serial number
            customer: Customer name
            
        Returns:
            True if successful
        """
        if serial_number not in self._items:
            print(f"Error: Item {serial_number} not found")
            return False
            
        item = self._items[serial_number]
        if item.status != "in_stock":
            print(f"Error: Item {serial_number} is {item.status}, cannot ship")
            return False
            
        if item.ship(customer):
            self._log_transaction("SHIP", serial_number, item.name, customer=customer)
            print(f"Shipped: {serial_number} - {item.name} to {customer}")
            return True
        return False
        
    def get_item(self, serial_number: str) -> Optional[TrackedItem]:
        """
        Get a specific tracked item
        
        Args:
            serial_number: Item's serial number
            
        Returns:
            TrackedItem or None
        """
        return self._items.get(serial_number)
        
    def get_all_items(self, status: str = None) -> List[TrackedItem]:
        """
        Get all items, optionally filtered by status
        
        Args:
            status: Filter by status (in_stock, shipped, damaged)
            
        Returns:
            List of TrackedItems
        """
        if status:
            return [item for item in self._items.values() if item.status == status]
        return list(self._items.values())
        
    def get_stock_summary(self) -> str:
        """
        Get formatted stock summary
        
        Returns:
            Formatted string
        """
        in_stock = self.get_all_items("in_stock")
        shipped = self.get_all_items("shipped")
        damaged = self.get_all_items("damaged")
        
        summary = f"\n{'='*60}\n"
        summary += f"TRACKED WAREHOUSE - {self.name}\n"
        summary += f"{'='*60}\n"
        summary += f"Total Items: {len(self._items)}\n"
        summary += f"  In Stock: {len(in_stock)}\n"
        summary += f"  Shipped:  {len(shipped)}\n"
        summary += f"  Damaged:  {len(damaged)}\n"
        summary += f"{'='*60}\n"
        
        if in_stock:
            summary += f"\nIN STOCK ITEMS:\n"
            summary += f"{'Serial':<14} {'Name':<20} {'Location':<15} {'Supplier':<15}\n"
            summary += f"{'-'*64}\n"
            for item in in_stock:
                summary += (f"{item.serial_number:<14} {item.name:<20} "
                          f"{item.location:<15} {item.supplier:<15}\n")
                          
        return summary
        
    def get_item_history(self, serial_number: str) -> Optional[str]:
        """
        Get the full history of an item
        
        Args:
            serial_number: Item's serial number
            
        Returns:
            Formatted history string
        """
        item = self.get_item(serial_number)
        if not item:
            return None
            
        info = item.get_info()
        history = f"\n{'='*50}\n"
        history += f"ITEM HISTORY: {serial_number}\n"
        history += f"{'='*50}\n"
        history += f"Name: {info['name']}\n"
        history += f"Status: {info['status']}\n"
        history += f"Received: {info['received_date']}\n"
        history += f"Supplier: {info['supplier']}\n"
        history += f"Location: {info['location']}\n"
        
        if info['status'] == 'shipped':
            history += f"Shipped: {info['shipped_date']}\n"
            history += f"Customer: {info['customer']}\n"
            
        if info['notes']:
            history += f"\nNotes:\n"
            for note in info['notes']:
                history += f"  {note}\n"
                
        history += f"{'='*50}\n"
        return history
        
    def move_item(self, serial_number: str, new_location: str) -> bool:
        """
        Move an item to a new location
        
        Args:
            serial_number: Item's serial number
            new_location: New warehouse location
            
        Returns:
            True if successful
        """
        item = self.get_item(serial_number)
        if not item:
            print(f"Error: Item {serial_number} not found")
            return False
            
        item.move_location(new_location)
        self._log_transaction("MOVE", serial_number, item.name, location=new_location)
        print(f"Moved: {serial_number} → {new_location}")
        return True
        
    def search_items(self, query: str) -> List[TrackedItem]:
        """
        Search items by name, serial, or location
        
        Args:
            query: Search term
            
        Returns:
            Matching TrackedItems
        """
        query = query.lower()
        results = []
        for item in self._items.values():
            if (query in item.name.lower() or 
                query in item.serial_number.lower() or
                query in item.location.lower() or
                query in item.supplier.lower() or
                query in item.status.lower()):
                results.append(item)
        return results
        
    def _log_transaction(self, action: str, serial_number: str, name: str = "",
                        supplier: str = "", customer: str = "", location: str = ""):
        """Log a transaction"""
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "serial_number": serial_number,
            "name": name
        }
        if supplier:
            transaction["supplier"] = supplier
        if customer:
            transaction["customer"] = customer
        if location:
            transaction["location"] = location
            
        self._transaction_log.append(transaction)
        
    def get_transaction_history(self, limit: int = 20) -> list:
        """Get recent transactions"""
        return self._transaction_log[-limit:]