"""
Warehouse class for Warehouse Management System Tier 1
Handles bulk storage tracking
"""

from typing import Dict, Optional
from .item import Item

class Warehouse:
    """
    Represents a warehouse with bulk storage capabilities
    Tracks quantities of items (Tier 1)
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
        self._inventory: Dict[str, dict] = {}  # item_id -> {"item": Item, "quantity": int}
        self._transaction_log: list = []
        
    def add_item(self, item: Item, quantity: int) -> bool:
        """
        Add items to the warehouse
        
        Args:
            item: Item object to add
            quantity: Quantity to add (must be positive)
            
        Returns:
            True if successful, False otherwise
        """
        if quantity <= 0:
            print(f"Error: Quantity must be positive. Got {quantity}")
            return False
            
        if item.item_id in self._inventory:
            self._inventory[item.item_id]["quantity"] += quantity
        else:
            self._inventory[item.item_id] = {
                "item": item,
                "quantity": quantity
            }
            
        self._log_transaction("ADD", item.item_id, quantity, item.name)
        print(f"Successfully added {quantity} units of {item.name} (ID: {item.item_id})")
        return True
        
    def remove_item(self, item_id: str, quantity: int) -> bool:
        """
        Remove items from the warehouse
        
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
            
        if self._inventory[item_id]["quantity"] < quantity:
            print(f"Error: Insufficient stock. Requested: {quantity}, Available: {self._inventory[item_id]['quantity']}")
            return False
            
        self._inventory[item_id]["quantity"] -= quantity
        item_name = self._inventory[item_id]["item"].name
        
        # Remove item entry if quantity reaches 0
        if self._inventory[item_id]["quantity"] == 0:
            del self._inventory[item_id]
            
        self._log_transaction("REMOVE", item_id, quantity, item_name)
        print(f"Successfully removed {quantity} units of {item_name} (ID: {item_id})")
        return True
        
    def check_stock(self, item_id: str = None) -> dict:
        """
        Check stock levels
        
        Args:
            item_id: Optional item ID to check specific item
            
        Returns:
            Dictionary with stock information
        """
        if item_id:
            if item_id in self._inventory:
                item_data = self._inventory[item_id]
                return {
                    "item": item_data["item"].get_info(),
                    "quantity": item_data["quantity"]
                }
            else:
                return {"error": f"Item with ID '{item_id}' not found"}
        else:
            # Return all stock
            stock = {}
            for item_id, item_data in self._inventory.items():
                stock[item_id] = {
                    "item": item_data["item"].get_info(),
                    "quantity": item_data["quantity"]
                }
            return stock
            
    def get_stock_summary(self) -> str:
        """
        Get a formatted summary of current stock
        
        Returns:
            Formatted string with stock information
        """
        if not self._inventory:
            return "Warehouse is empty"
            
        summary = f"\n{'='*50}\n"
        summary += f"WAREHOUSE STOCK SUMMARY - {self.name}\n"
        summary += f"{'='*50}\n"
        summary += f"{'ID':<10} {'Name':<20} {'Quantity':<10} {'Unit Price':<10}\n"
        summary += f"{'-'*50}\n"
        
        total_value = 0
        total_items = 0
        
        for item_id, item_data in self._inventory.items():
            item = item_data["item"]
            quantity = item_data["quantity"]
            value = quantity * item.unit_price
            
            summary += f"{item_id:<10} {item.name:<20} {quantity:<10} ${item.unit_price:<9.2f}\n"
            total_value += value
            total_items += quantity
            
        summary += f"{'-'*50}\n"
        summary += f"TOTAL: {total_items} items, Total Value: ${total_value:.2f}\n"
        summary += f"{'='*50}\n"
        
        return summary
        
    def get_item_info(self, item_id: str) -> Optional[dict]:
        """
        Get detailed information about a specific item
        
        Args:
            item_id: ID of the item
            
        Returns:
            Dictionary with item information or None if not found
        """
        if item_id in self._inventory:
            item_data = self._inventory[item_id]
            return {
                "item": item_data["item"].get_info(),
                "quantity": item_data["quantity"]
            }
        return None
        
    def _log_transaction(self, action: str, item_id: str, quantity: int, item_name: str = ""):
        """
        Log a transaction
        
        Args:
            action: Type of transaction (ADD/REMOVE)
            item_id: ID of the item
            quantity: Quantity involved
            item_name: Name of the item
        """
        from datetime import datetime
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "item_id": item_id,
            "item_name": item_name,
            "quantity": quantity
        }
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