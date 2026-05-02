"""
Main entry point for Warehouse Management System Tier 3
"""

from .tracked_ui import TrackedUI

def main():
    """
    Main function to run the Warehouse Management System
    """
    ui = TrackedUI()
    ui.start()

if __name__ == "__main__":
    main()