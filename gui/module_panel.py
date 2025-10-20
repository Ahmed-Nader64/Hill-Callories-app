"""
Module panel for HeroCal application.
Displays available calculation modules organized by category.
"""

from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTreeWidget, QTreeWidgetItem, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from core.base_module import ModuleInfo


class ModulePanel(QWidget):
    """Panel displaying available calculation modules"""
    
    module_selected = pyqtSignal(str)  # Emitted when a module is selected
    
    def __init__(self, calculation_engine):
        super().__init__()
        self.calculation_engine = calculation_engine
        self.setup_ui()
        self.populate_modules()
    
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Calculation Modules")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Module tree
        self.module_tree = QTreeWidget()
        self.module_tree.setHeaderHidden(True)
        self.module_tree.itemClicked.connect(self.on_module_clicked)
        layout.addWidget(self.module_tree)
        
        # Recent projects section
        recent_group = QGroupBox("Recent Projects")
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_list = QTreeWidget()
        self.recent_list.setHeaderHidden(True)
        self.recent_list.setMaximumHeight(150)
        recent_layout.addWidget(self.recent_list)
        
        layout.addWidget(recent_group)
    
    def populate_modules(self):
        """Populate the module tree with available modules"""
        self.module_tree.clear()
        
        # Get modules by category
        categories = self.calculation_engine.get_module_categories()
        
        for category, module_names in categories.items():
            # Create category item
            category_item = QTreeWidgetItem(self.module_tree)
            category_item.setText(0, self.get_category_icon(category) + f" {category}")
            category_item.setData(0, Qt.ItemDataRole.UserRole, None)  # No module data for categories
            
            # Add modules to category
            for module_name in module_names:
                module_item = QTreeWidgetItem(category_item)
                module_info = self.calculation_engine.get_module_info(module_name)
                if module_info:
                    module_item.setText(0, f"  • {module_info.name}")
                    module_item.setData(0, Qt.ItemDataRole.UserRole, module_name)
                    module_item.setToolTip(0, module_info.description)
            
            # Expand category
            category_item.setExpanded(True)
    
    def get_category_icon(self, category: str) -> str:
        """Get icon for category"""
        icons = {
            "Structural": "📐",
            "Electrical": "⚡",
            "Thermal": "🔥",
            "Mechanical": "🔧",
            "Custom": "📦"
        }
        return icons.get(category, "📋")
    
    def on_module_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle module selection"""
        module_name = item.data(0, Qt.ItemDataRole.UserRole)
        if module_name:
            self.module_selected.emit(module_name)
    
    def update_recent_projects(self, projects: List[Dict]):
        """Update the recent projects list"""
        self.recent_list.clear()
        
        for project in projects:
            item = QTreeWidgetItem(self.recent_list)
            item.setText(0, f"📄 {project.get('name', 'Unnamed Project')}")
            item.setToolTip(0, f"Modified: {project.get('modified_date', 'Unknown')}")
            item.setData(0, Qt.ItemDataRole.UserRole, project)
    
    def refresh_modules(self):
        """Refresh the module list"""
        self.populate_modules()
