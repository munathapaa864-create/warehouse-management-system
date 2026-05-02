"""
Warehouse class for Warehouse Management System Tier 2
Handles FIFO batch tracking
"""

from typing import Dict, List, Optional
from datetime import datetime
from .item import Item
from .batch import Batch

class Warehouse:
    """
    Represents a warehouse with FIFO batch tracking (Tier 2)
    Tracks batches and implements First-In-First-Out logic
    """
    
    def __init__(self, name: str = "Main Warehouse", location: str = "Default Location"):
        """
        Initialize the warehouse
        
        Args:
            name: Name of the warehouse
            location: Physical location of the warehouse
        """
        self.name = name
        self.location = location
        self._inventory: Dict[str, dict] = {}  # item_id -> {"item": Item, "batches": List[Batch]}
        self._transaction_log: list = []
        
    def add_item(self, item: Item, quantity: int, supplier: str = "Unknown", 
                 received_date: Optional[datetime] = None, unit_price: Optional[float] = None) -> bool:
        """
        Add items to warehouse as a new batch
        
        Args:
            item: Item object to add
            quantity: Quantity to add (must be positive)
            supplier: Name of the supplier
            received_date: Date when received (defaults to now)
            unit_price: Price per unit (defaults to item's price)
            
        Returns:
            True if successful, False otherwise
        """
        if quantity <= 0:
            print(f"Error: Quantity must be positive. Got {quantity}")
            return False
            
        # Use item's price if not specified
        if unit_price is None:
            unit_price = item.unit_price
            
        # Create new batch
        new_batch = Batch(
            received_date=received_date or datetime.now(),
            supplier=supplier,
            quantity=quantity,
            unit_price=unit_price
        )
        
        # Add to inventory
        if item.item_id not in self._inventory:
            self._inventory[item.item_id] = {
                "item": item,
                "batches": []
            }
            
        self._inventory[item.item_id]["batches"].append(new_batch)
        
        self._log_transaction("ADD", item.item_id, quantity, item.name, 
                             batch_id=new_batch.batch_id, supplier=supplier)
        print(f"Successfully added {quantity} units of {item.name} "
              f"in batch {new_batch.batch_id} from {supplier}")
        return True
        
    def remove_item(self, item_id: str, quantity: int) -> bool:
        """
        Remove items from warehouse using FIFO logic
        
        Args:
            item_id: ID of the item to remove
            quantity: Quantity to remove (must be positive)
            
        Returns:
            True if successful, False otherwise
        """
        if quantity <= 0:
            print(f"Error: Quantity must be positive. Got {quantity}")
            return False
            
        if item_id not in self._inventory:
            print(f"Error: Item with ID '{item_id}' not found in warehouse")
            return False
            
        # Check total available quantity
        total_available = self._get_total_quantity(item_id)
        if total_available < quantity:
            print(f"Error: Insufficient stock. Requested: {quantity}, Available: {total_available}")
            return False
            
        # FIFO: Remove from oldest batches first
        remaining_to_remove = quantity
        batches_removed = []
        
        # Sort batches by received date (oldest first)
        sorted_batches = sorted(self._inventory[item_id]["batches"])
        
        for batch in sorted_batches:
            if remaining_to_remove <= 0:
                break
                
            removed, is_depleted = batch.remove_quantity(remaining_to_remove)
            if removed > 0:
                batches_removed.append({
                    "batch_id": batch.batch_id,
                    "quantity": removed,
                    "depleted": is_depleted
                })
                remaining_to_remove -= removed
                
        # Remove depleted batches
        self._inventory[item_id]["batches"] = [
            b for b in self._inventory[item_id]["batches"] if b.quantity > 0
        ]
        
        # Remove item entry if no batches left
        if len(self._inventory[item_id]["batches"]) == 0:
            del self._inventory[item_id]
            
        item_name = self._inventory.get(item_id, {}).get("item", Item(item_id, "Unknown")).name
        if item_id not in self._inventory:
            item_name = "Unknown"
            
        self._log_transaction("REMOVE", item_id, quantity, item_name, 
                             batch_details=batches_removed)
        
        print(f"Successfully removed {quantity} units using FIFO:")
        for batch_info in batches_removed:
            print(f"  - {batch_info['quantity']} from batch {batch_info['batch_id']}")
            
        return True
        
    def check_stock(self, item_id: str = None) -> dict:
        """
        Check stock levels with batch information
        
        Args:
            item_id: Optional item ID to check specific item
            
        Returns:
            Dictionary with stock information including batches
        """
        if item_id:
            if item_id in self._inventory:
                item_data = self._inventory[item_id]
                batches_info = []
                total_qty = 0
                total_value = 0
                
                # Sort batches by date for display
                sorted_batches = sorted(item_data["batches"])
                
                for batch in sorted_batches:
                    batches_info.append(batch.get_info())
                    total_qty += batch.quantity
                    total_value += batch.get_value()
                    
                return {
                    "item": item_data["item"].get_info(),
                    "total_quantity": total_qty,
                    "total_value": total_value,
                    "batch_count": len(sorted_batches),
                    "batches": batches_info
                }
            else:
                return {"error": f"Item with ID '{item_id}' not found"}
        else:
            # Return all stock
            stock = {}
            for item_id, item_data in self._inventory.items():
                batches_info = []
                total_qty = 0
                total_value = 0
                
                sorted_batches = sorted(item_data["batches"])
                
                for batch in sorted_batches:
                    batches_info.append(batch.get_info())
                    total_qty += batch.quantity
                    total_value += batch.get_value()
                    
                stock[item_id] = {
                    "item": item_data["item"].get_info(),
                    "total_quantity": total_qty,
                    "total_value": total_value,
                    "batch_count": len(sorted_batches),
                    "batches": batches_info
                }
            return stock
            
    def get_stock_summary(self) -> str:
        """
        Get a formatted summary of current stock with batch information
        
        Returns:
            Formatted string with stock information
        """
        if not self._inventory:
            return "Warehouse is empty"
            
        summary = f"\n{'='*70}\n"
        summary += f"WAREHOUSE STOCK SUMMARY (FIFO) - {self.name}\n"
        summary += f"{'='*70}\n"
        
        total_value = 0
        total_items = 0
        
        for item_id, item_data in self._inventory.items():
            item = item_data["item"]
            sorted_batches = sorted(item_data["batches"])
            
            item_total_qty = sum(b.quantity for b in sorted_batches)
            item_total_value = sum(b.get_value() for b in sorted_batches)
            
            summary += f"\nItem: {item.name} (ID: {item_id})\n"
            summary += f"Description: {item.description}\n"
            summary += f"Total Quantity: {item_total_qty} | Total Value: ${item_total_value:.2f}\n"
            summary += f"Batches ({len(sorted_batches)}):\n"
            summary += f"  {'Batch ID':<12} {'Received':<20} {'Supplier':<15} {'Qty':<8} {'Price':<10} {'Value':<10}\n"
            summary += f"  {'-'*75}\n"
            
            for batch in sorted_batches:
                info = batch.get_info()
                summary += (f"  {info['batch_id']:<12} "
                          f"{info['received_date']:<20} "
                          f"{info['supplier']:<15} "
                          f"{info['quantity']:<8} "
                          f"${info['unit_price']:<9.2f} "
                          f"${info['total_value']:<9.2f}\n")
                
            total_value += item_total_value
            total_items += item_total_qty
            
        summary += f"\n{'='*70}\n"
        summary += f"TOTAL: {total_items} items in stock | Total Value: ${total_value:.2f}\n"
        summary += f"{'='*70}\n"
        
        return summary
        
    def get_item_info(self, item_id: str) -> Optional[dict]:
        """
        Get detailed information about a specific item including batches
        
        Args:
            item_id: ID of the item
            
        Returns:
            Dictionary with item and batch information or None if not found
        """
        return self.check_stock(item_id)
        
    def get_fifo_queue(self, item_id: str) -> list:
        """
        Get the FIFO queue for a specific item
        
        Args:
            item_id: ID of the item
            
        Returns:
            List of batches sorted by age (oldest first)
        """
        if item_id not in self._inventory:
            return []
            
        return sorted(self._inventory[item_id]["batches"])
        
    def _get_total_quantity(self, item_id: str) -> int:
        """
        Get total quantity of an item across all batches
        
        Args:
            item_id: ID of the item
            
        Returns:
            Total quantity
        """
        if item_id not in self._inventory:
            return 0
            
        return sum(batch.quantity for batch in self._inventory[item_id]["batches"])
        
    def _log_transaction(self, action: str, item_id: str, quantity: int, 
                        item_name: str = "", batch_id: str = "", supplier: str = "",
                        batch_details: list = None):
        """
        Log a transaction with batch information
        
        Args:
            action: Type of transaction (ADD/REMOVE)
            item_id: ID of the item
            quantity: Quantity involved
            item_name: Name of the item
            batch_id: Batch ID (for additions)
            supplier: Supplier name (for additions)
            batch_details: List of batch details (for removals)
        """
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "item_id": item_id,
            "item_name": item_name,
            "quantity": quantity
        }
        
        if action == "ADD":
            transaction["batch_id"] = batch_id
            transaction["supplier"] = supplier
        elif action == "REMOVE" and batch_details:
            transaction["batch_details"] = batch_details
            
        self._transaction_log.append(transaction)
        
    def get_transaction_history(self, limit: int = None) -> list:
        """
        Get transaction history
        
        Args:
            limit: Optional limit on number of transactions to return
            
        Returns:
            List of transactions
        """
        if limit:
            return self._transaction_log[-limit:]
        return self._transaction_log
        
    def get_batch_details(self, batch_id: str) -> Optional[dict]:
        """
        Find and return details of a specific batch
        
        Args:
            batch_id: ID of the batch to find
            
        Returns:
            Dictionary with batch and item info, or None if not found
        """
        for item_id, item_data in self._inventory.items():
            for batch in item_data["batches"]:
                if batch.batch_id == batch_id:
                    return {
                        "item": item_data["item"].get_info(),
                        "batch": batch.get_info()
                    }
        return None