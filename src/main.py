"""
Main entry point for Warehouse Management System Tier 2
"""

from .ui import UserInterface

def main():
    """
    Main function to run the Warehouse Management System
    """
    ui = UserInterface()
    ui.start()

if __name__ == "__main__":
    main()