#!/usr/bin/env python3
"""
HeroCal - Engineering Calculator Application
A comprehensive calculator with GUI, mathematical functions, and data visualization.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

from gui.main_window import MainWindow

def setup_logging():
    """Set up application logging"""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'engicalc.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the HeroCal application."""
    try:
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting HeroCal application")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("HeroCal")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("HeroCal")
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show the main window
        window = MainWindow()
        window.show()
        
        logger.info("HeroCal application started successfully")
        
        # Start the event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logging.error(f"Failed to start HeroCal application: {e}")
        if 'app' in locals():
            QMessageBox.critical(None, "Startup Error", f"Failed to start HeroCal:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
