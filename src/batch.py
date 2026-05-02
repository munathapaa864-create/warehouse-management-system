"""
Batch class for Warehouse Management System Tier 2
Represents a batch of items with FIFO tracking
"""

from datetime import datetime
from typing import Optional

class Batch:
    """
    Represents a batch of items received at a specific time
    Used for FIFO (First-In-First-Out) inventory management
    """
    
    _batch_counter = 1  # Class variable for generating unique batch IDs
    
    def __init__(self, batch_id: Optional[str] = None, received_date: Optional[datetime] = None, 
                 supplier: str = "", quantity: int = 0, unit_price: float = 0.0):
        """
        Initialize a batch
        
        Args:
            batch_id: Unique identifier for the batch (auto-generated if not provided)
            received_date: Date when batch was received (defaults to now)
            supplier: Name of the supplier
            quantity: Initial quantity in the batch
            unit_price: Price per unit for this batch
        """
        if batch_id:
            self.batch_id = batch_id
        else:
            self.batch_id = f"BATCH-{Batch._batch_counter:04d}"
            Batch._batch_counter += 1
            
        self.received_date = received_date or datetime.now()
        self.supplier = supplier
        self.quantity = quantity
        self.unit_price = unit_price
        
    def remove_quantity(self, quantity: int) -> tuple[int, bool]:
        """
        Remove quantity from batch
        
        Args:
            quantity: Amount to remove
            
        Returns:
            Tuple of (actual_removed, is_batch_depleted)
        """
        if quantity <= 0:
            return 0, False
            
        if quantity >= self.quantity:
            removed = self.quantity
            self.quantity = 0
            return removed, True
        else:
            self.quantity -= quantity
            return quantity, False
            
    def add_quantity(self, quantity: int) -> bool:
        """
        Add quantity to batch
        
        Args:
            quantity: Amount to add
            
        Returns:
            True if successful, False otherwise
        """
        if quantity <= 0:
            return False
        self.quantity += quantity
        return True
        
    def get_value(self) -> float:
        """
        Calculate total value of the batch
        
        Returns:
            Total value
        """
        return self.quantity * self.unit_price
        
    def get_info(self) -> dict:
        """
        Get batch information as dictionary
        
        Returns:
            Dictionary with batch details
        """
        return {
            "batch_id": self.batch_id,
            "received_date": self.received_date.strftime("%Y-%m-%d %H:%M:%S"),
            "supplier": self.supplier,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_value": self.get_value()
        }
        
    def __str__(self) -> str:
        """String representation of the batch"""
        return (f"Batch(id={self.batch_id}, "
                f"date={self.received_date.strftime('%Y-%m-%d')}, "
                f"qty={self.quantity}, price=${self.unit_price:.2f})")
    
    def __lt__(self, other) -> bool:
        """Compare batches by received date for FIFO ordering"""
        if isinstance(other, Batch):
            return self.received_date < other.received_date
        return NotImplemented