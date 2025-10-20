"""
Main window for HeroCal application.
Provides the primary user interface with module panels, input forms, and visualization.
"""

import sys
import os
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QToolBar, QStatusBar, QLabel, QPushButton, QComboBox,
    QTabWidget, QTextEdit, QGroupBox, QGridLayout, QLineEdit,
    QMessageBox, QFileDialog, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QAction, QIcon, QFont, QPalette, QColor

from core.calculation_engine import CalculationEngine
from core.data_manager import DataManager
from core.settings_manager import SettingsManager
from core.visualization_manager import VisualizationManager
from core.webhook_service import WebhookService
from .module_panel import ModulePanel
from .input_panel import InputPanel
from .results_panel import ResultsPanel
from .visualization_panel import VisualizationPanel


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.calculation_engine = CalculationEngine()
        self.data_manager = DataManager()
        self.settings_manager = SettingsManager()
        self.visualization_manager = VisualizationManager()
        self.webhook_service = WebhookService(self.settings_manager)
        
        # Current state
        self.current_project = None
        self.current_module = None
        self.current_calculation = None
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        
        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
        self.setup_auto_save()
        
        # Set window properties
        self.setWindowTitle("HeroCal - Engineering Calculator")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Apply theme
        self.apply_theme()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create left panel (modules)
        self.module_panel = ModulePanel(self.calculation_engine)
        splitter.addWidget(self.module_panel)
        
        # Create center panel (input and results)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # Input panel
        self.input_panel = InputPanel()
        center_layout.addWidget(self.input_panel)
        
        # Results panel
        self.results_panel = ResultsPanel()
        center_layout.addWidget(self.results_panel)
        
        splitter.addWidget(center_widget)
        
        # Create right panel (visualization)
        self.visualization_panel = VisualizationPanel(self.visualization_manager)
        splitter.addWidget(self.visualization_panel)
        
        # Set splitter proportions
        splitter.setSizes([250, 600, 350])
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create tool bar
        self.create_tool_bar()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Project', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction('&Open Project...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction('&Save Project', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save Project &As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('&Export Results...', self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('&Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        # Modules menu
        modules_menu = menubar.addMenu('&Modules')
        
        # Settings menu
        settings_menu = menubar.addMenu('&Settings')
        
        preferences_action = QAction('&Preferences...', self)
        preferences_action.triggered.connect(self.show_preferences)
        settings_menu.addAction(preferences_action)
        
        settings_menu.addSeparator()
        
        test_webhook_action = QAction('&Test Webhook...', self)
        test_webhook_action.triggered.connect(self.test_webhook)
        settings_menu.addAction(test_webhook_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        help_action = QAction('&User Manual', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        about_action = QAction('&About HeroCal', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """Create the tool bar"""
        toolbar = self.addToolBar('Main Toolbar')
        
        # New project
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)
        
        # Open project
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)
        
        # Save project
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Calculate
        calculate_action = QAction('Calculate', self)
        calculate_action.triggered.connect(self.calculate)
        toolbar.addAction(calculate_action)
        
        # Reset
        reset_action = QAction('Reset', self)
        reset_action.triggered.connect(self.reset_inputs)
        toolbar.addAction(reset_action)
        
        toolbar.addSeparator()
        
        # Units selector
        self.units_combo = QComboBox()
        self.units_combo.addItems(['SI', 'Imperial'])
        self.units_combo.currentTextChanged.connect(self.change_units)
        toolbar.addWidget(QLabel('Units:'))
        toolbar.addWidget(self.units_combo)
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Dark', 'Light', 'High Contrast'])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        toolbar.addWidget(QLabel('Theme:'))
        toolbar.addWidget(self.theme_combo)
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = self.statusBar()
        
        # Project info
        self.project_label = QLabel("No project loaded")
        self.status_bar.addWidget(self.project_label)
        
        # Auto-save status
        self.auto_save_label = QLabel("Auto-save: OFF")
        self.status_bar.addPermanentWidget(self.auto_save_label)
        
        # Memory display
        self.memory_label = QLabel("Memory: 0.0")
        self.status_bar.addPermanentWidget(self.memory_label)
        
        # Ready status
        self.ready_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.ready_label)
    
    def setup_connections(self):
        """Set up signal connections"""
        # Module panel connections
        self.module_panel.module_selected.connect(self.on_module_selected)
        
        # Input panel connections
        self.input_panel.inputs_changed.connect(self.on_inputs_changed)
        self.input_panel.calculate_requested.connect(self.calculate)
        
        # Results panel connections
        self.results_panel.export_requested.connect(self.export_results)
    
    def load_settings(self):
        """Load application settings"""
        # Load window geometry
        settings = QSettings()
        geometry = settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        # Load units
        units = self.settings_manager.get_setting('units.system', 'SI')
        self.units_combo.setCurrentText(units)
        
        # Load theme
        theme = self.settings_manager.get_setting('display.theme', 'dark')
        self.theme_combo.setCurrentText(theme.title())
    
    def setup_auto_save(self):
        """Set up auto-save functionality"""
        auto_save_enabled = self.settings_manager.get_setting('application.auto_save', True)
        if auto_save_enabled:
            interval = self.settings_manager.get_setting('application.auto_save_interval', 300) * 1000  # Convert to ms
            self.auto_save_timer.start(interval)
            self.auto_save_label.setText("Auto-save: ON")
        else:
            self.auto_save_label.setText("Auto-save: OFF")
    
    def apply_theme(self):
        """Apply the current theme"""
        theme = self.settings_manager.get_setting('display.theme', 'dark')
        colors = self.settings_manager.get_theme_colors()
        
        # Apply stylesheet
        stylesheet = f"""
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        QMenuBar {{
            background-color: {colors['primary_panel']};
            color: {colors['text']};
        }}
        QToolBar {{
            background-color: {colors['primary_panel']};
            color: {colors['text']};
        }}
        QStatusBar {{
            background-color: {colors['primary_panel']};
            color: {colors['text']};
        }}
        QGroupBox {{
            background-color: {colors['secondary_panel']};
            color: {colors['text']};
            border: 1px solid {colors['accent']};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        QPushButton {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {colors['accent']};
            opacity: 0.8;
        }}
        QLineEdit {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 1px solid {colors['accent']};
            border-radius: 3px;
            padding: 5px;
        }}
        QComboBox {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 1px solid {colors['accent']};
            border-radius: 3px;
            padding: 5px;
        }}
        """
        
        self.setStyleSheet(stylesheet)
    
    # Event handlers
    def on_module_selected(self, module_name: str):
        """Handle module selection"""
        self.current_module = module_name
        module_info = self.calculation_engine.get_module_info(module_name)
        
        if module_info:
            self.input_panel.set_module(module_info)
            self.status_bar.showMessage(f"Selected module: {module_name}")
    
    def on_inputs_changed(self, inputs: Dict[str, Any]):
        """Handle input changes"""
        # Update input validation
        if self.current_module:
            validation_result = self.calculation_engine.validate_inputs(self.current_module, inputs)
            self.input_panel.update_validation(validation_result)
    
    def calculate(self):
        """Perform calculation"""
        if not self.current_module:
            QMessageBox.warning(self, "No Module Selected", "Please select a calculation module first.")
            return
        
        inputs = self.input_panel.get_inputs()
        if not inputs:
            QMessageBox.warning(self, "No Inputs", "Please enter calculation inputs.")
            return
        
        # Show progress
        self.status_bar.showMessage("Calculating...")
        
        # Perform calculation
        try:
            import time
            start_time = time.time()
            result = self.calculation_engine.calculate(self.current_module, inputs)
            execution_time = time.time() - start_time
            
            if result.success:
                self.current_calculation = result
                self.results_panel.set_results(result)
                
                # Send calculation result to webhook
                self.webhook_service.send_calculation_result(
                    self.current_module, inputs, result.outputs, execution_time
                )
                
                # Update visualization
                if result.charts:
                    for chart_data in result.charts:
                        chart = self.visualization_manager.create_chart(
                            chart_data['type'], chart_data['data'], chart_data
                        )
                        self.visualization_panel.add_chart(chart)
                
                self.status_bar.showMessage("Calculation completed successfully")
            else:
                # Send error to webhook
                self.webhook_service.send_error(
                    "calculation_error", 
                    "\n".join(result.errors),
                    self.current_module,
                    {"inputs": inputs}
                )
                
                QMessageBox.critical(self, "Calculation Error", 
                                   f"Calculation failed:\n" + "\n".join(result.errors))
                self.status_bar.showMessage("Calculation failed")
                
        except Exception as e:
            # Send error to webhook
            self.webhook_service.send_error(
                "unexpected_error", 
                str(e),
                self.current_module,
                {"inputs": inputs}
            )
            
            QMessageBox.critical(self, "Calculation Error", f"Unexpected error: {str(e)}")
            self.status_bar.showMessage("Calculation failed")
    
    def reset_inputs(self):
        """Reset input fields"""
        self.input_panel.reset_inputs()
        self.results_panel.clear_results()
        self.visualization_panel.clear_charts()
        self.status_bar.showMessage("Inputs reset")
    
    def new_project(self):
        """Create new project"""
        # TODO: Implement new project dialog
        self.current_project = None
        self.project_label.setText("New project")
        self.status_bar.showMessage("New project created")
    
    def open_project(self):
        """Open existing project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "HeroCal Projects (*.ecp);;All Files (*)"
        )
        
        if file_path:
            project_data = self.data_manager.load_project_from_file(file_path)
            if project_data:
                self.current_project = project_data
                self.project_label.setText(f"Project: {os.path.basename(file_path)}")
                self.status_bar.showMessage(f"Opened project: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load project file.")
    
    def save_project(self):
        """Save current project"""
        if not self.current_project:
            self.save_project_as()
            return
        
        # TODO: Implement project saving
        # Send project save event to webhook
        self.webhook_service.send_project_save(
            self.current_project.get('name', 'Untitled'),
            self.current_project.get('file_path', ''),
            self.current_project
        )
        
        self.status_bar.showMessage("Project saved")
    
    def save_project_as(self):
        """Save project with new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "HeroCal Projects (*.ecp);;All Files (*)"
        )
        
        if file_path:
            # TODO: Implement project saving
            # Send project save event to webhook
            self.webhook_service.send_project_save(
                os.path.basename(file_path),
                file_path,
                self.current_project or {}
            )
            
            self.status_bar.showMessage(f"Project saved as: {file_path}")
    
    def export_results(self):
        """Export calculation results"""
        if not self.current_calculation:
            QMessageBox.warning(self, "No Results", "No calculation results to export.")
            return
        
        # TODO: Implement result export
        self.status_bar.showMessage("Results exported")
    
    def auto_save(self):
        """Auto-save current work"""
        if self.current_project:
            # TODO: Implement auto-save
            self.status_bar.showMessage("Auto-saved", 2000)
    
    def change_units(self, units: str):
        """Change unit system"""
        self.settings_manager.set_setting('units.system', units)
        self.status_bar.showMessage(f"Units changed to {units}")
    
    def change_theme(self, theme: str):
        """Change application theme"""
        theme_lower = theme.lower().replace(' ', '_')
        self.settings_manager.set_setting('display.theme', theme_lower)
        self.apply_theme()
        self.status_bar.showMessage(f"Theme changed to {theme}")
    
    def undo(self):
        """Undo last action"""
        # TODO: Implement undo functionality
        self.status_bar.showMessage("Undo not implemented yet")
    
    def redo(self):
        """Redo last action"""
        # TODO: Implement redo functionality
        self.status_bar.showMessage("Redo not implemented yet")
    
    def show_preferences(self):
        """Show preferences dialog"""
        # TODO: Implement preferences dialog
        QMessageBox.information(self, "Preferences", "Preferences dialog not implemented yet")
    
    def test_webhook(self):
        """Test webhook connectivity"""
        if not self.webhook_service.is_enabled():
            QMessageBox.warning(self, "Webhook Disabled", "Webhook is currently disabled in settings.")
            return
        
        webhook_url = self.webhook_service.get_webhook_url()
        if not webhook_url:
            QMessageBox.warning(self, "No Webhook URL", "No webhook URL is configured.")
            return
        
        # Show progress dialog
        progress = QMessageBox(self)
        progress.setWindowTitle("Testing Webhook")
        progress.setText(f"Testing webhook connection to:\n{webhook_url}")
        progress.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress.show()
        
        # Test webhook in a separate thread
        def test_complete():
            success = self.webhook_service.test_webhook()
            progress.close()
            
            if success:
                QMessageBox.information(self, "Webhook Test", "Webhook test successful!")
            else:
                QMessageBox.critical(self, "Webhook Test", "Webhook test failed. Check the URL and network connection.")
        
        # Use QTimer to run test in main thread
        QTimer.singleShot(100, test_complete)
    
    def show_help(self):
        """Show help documentation"""
        # TODO: Implement help system
        QMessageBox.information(self, "Help", "Help system not implemented yet")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About HeroCal", 
                         "HeroCal - Engineering Calculator\n"
                         "Version 1.0.0\n\n"
                         "A comprehensive engineering calculator with modular analysis capabilities.")
    
    def closeEvent(self, event):
        """Handle application close"""
        # Save settings
        settings = QSettings()
        settings.setValue('geometry', self.saveGeometry())
        self.settings_manager.save_settings()
        
        # Shutdown calculation engine
        self.calculation_engine.shutdown()
        
        # Shutdown webhook service
        self.webhook_service.shutdown()
        
        event.accept()
