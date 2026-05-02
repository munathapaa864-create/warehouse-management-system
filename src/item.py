"""
Item class for Warehouse Management System
Represents a basic item with properties
"""

class Item:
    """
    Represents an item in the warehouse with basic information
    """
    
    def __init__(self, item_id: str, name: str, description: str = "", unit_price: float = 0.0):
        """
        Initialize an item
        
        Args:
            item_id: Unique identifier for the item
            name: Name of the item
            description: Optional description of the item
            unit_price: Price per unit of the item
        """
        self.item_id = item_id
        self.name = name
        self.description = description
        self.unit_price = unit_price
        
    def __str__(self) -> str:
        """String representation of the item"""
        return f"Item(id={self.item_id}, name={self.name}, price={self.unit_price})"
    
    def __eq__(self, other) -> bool:
        """Compare two items based on item_id"""
        if isinstance(other, Item):
            return self.item_id == other.item_id
        return False
    
    def get_info(self) -> dict:
        """
        Get item information as a dictionary
        
        Returns:
            Dictionary containing item details
        """
        return {
            "id": self.item_id,
            "name": self.name,
            "description": self.description,
            "unit_price": self.unit_price
        }