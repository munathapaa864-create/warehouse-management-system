"""
TrackedItem class for Warehouse Management System Tier 3
Represents an individual item with unique serial number tracking
"""

from datetime import datetime
from typing import Optional


class TrackedItem:
    """
    Represents a single tracked item with a unique serial number
    """
    
    _serial_counter = 1000
    
    def __init__(self, item_id: str, name: str, serial_number: Optional[str] = None,
                 description: str = "", unit_price: float = 0.0,
                 supplier: str = "", received_date: Optional[datetime] = None,
                 status: str = "in_stock"):
        """
        Initialize a tracked item
        
        Args:
            item_id: Product ID
            name: Product name
            serial_number: Unique serial number (auto-generated if None)
            description: Item description
            unit_price: Price per unit
            supplier: Where the item came from
            received_date: When the item was received
            status: Current status (in_stock, shipped, damaged, etc.)
        """
        self.item_id = item_id
        self.name = name
        
        if serial_number:
            self.serial_number = serial_number
        else:
            self.serial_number = f"SN-{TrackedItem._serial_counter:06d}"
            TrackedItem._serial_counter += 1
            
        self.description = description
        self.unit_price = unit_price
        self.supplier = supplier
        self.received_date = received_date or datetime.now()
        self.status = status
        self.shipped_date: Optional[datetime] = None
        self.customer: str = ""
        self.location: str = "Warehouse A"
        self.notes: list = []
        
    def ship(self, customer: str, ship_date: Optional[datetime] = None) -> bool:
        """
        Mark item as shipped
        
        Args:
            customer: Customer name
            ship_date: Date of shipping
            
        Returns:
            True if successful
        """
        if self.status != "in_stock":
            return False
            
        self.status = "shipped"
        self.shipped_date = ship_date or datetime.now()
        self.customer = customer
        self.add_note(f"Shipped to {customer}")
        return True
        
    def mark_damaged(self, reason: str = "") -> bool:
        """
        Mark item as damaged
        
        Args:
            reason: Reason for damage
            
        Returns:
            True if successful
        """
        self.status = "damaged"
        self.add_note(f"Damaged: {reason}" if reason else "Damaged")
        return True
        
    def move_location(self, new_location: str) -> bool:
        """
        Move item to a new location
        
        Args:
            new_location: New warehouse location
            
        Returns:
            True
        """
        old_location = self.location
        self.location = new_location
        self.add_note(f"Moved from {old_location} to {new_location}")
        return True
        
    def add_note(self, note: str):
        """Add a note to the item's history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notes.append(f"[{timestamp}] {note}")
        
    def get_info(self) -> dict:
        """
        Get complete item information
        
        Returns:
            Dictionary with all item details
        """
        return {
            "serial_number": self.serial_number,
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "unit_price": self.unit_price,
            "supplier": self.supplier,
            "received_date": self.received_date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "shipped_date": self.shipped_date.strftime("%Y-%m-%d %H:%M:%S") if self.shipped_date else "N/A",
            "customer": self.customer,
            "location": self.location,
            "notes": self.notes
        }
        
    def get_summary(self) -> str:
        """
        Get a short summary of the item
        
        Returns:
            Formatted string
        """
        return (f"{self.serial_number}: {self.name} "
                f"({self.status}) - {self.location}")
        
    def __str__(self) -> str:
        """String representation"""
        return f"TrackedItem(serial={self.serial_number}, name={self.name}, status={self.status})"
    
    def __eq__(self, other) -> bool:
        """Compare by serial number"""
        if isinstance(other, TrackedItem):
            return self.serial_number == other.serial_number
        return False