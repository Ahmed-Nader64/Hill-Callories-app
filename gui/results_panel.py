"""
Results panel for HeroCal application.
Displays calculation results and provides export functionality.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox, QTextEdit,
    QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from core.base_module import CalculationResult, OutputField


class ResultsPanel(QWidget):
    """Panel for displaying calculation results"""
    
    export_requested = pyqtSignal()  # Emitted when export is requested
    
    def __init__(self):
        super().__init__()
        self.current_result: CalculationResult = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("Results")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)
        
        # Status label
        self.status_label = QLabel("No calculation performed")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Parameter", "Value", "Unit"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        layout.addWidget(self.results_table)
        
        # Execution info
        self.execution_label = QLabel()
        self.execution_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.execution_label)
        
        # Error/warning display
        self.error_text = QTextEdit()
        self.error_text.setMaximumHeight(100)
        self.error_text.setStyleSheet("background-color: #ffebee; color: #c62828;")
        self.error_text.hide()
        layout.addWidget(self.error_text)
        
        self.warning_text = QTextEdit()
        self.warning_text.setMaximumHeight(100)
        self.warning_text.setStyleSheet("background-color: #fff3e0; color: #ef6c00;")
        self.warning_text.hide()
        layout.addWidget(self.warning_text)
        
        # Button panel
        button_layout = QHBoxLayout()
        
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_requested.emit)
        self.export_button.setEnabled(False)
        button_layout.addWidget(self.export_button)
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setEnabled(False)
        button_layout.addWidget(self.copy_button)
        
        layout.addLayout(button_layout)
    
    def set_results(self, result: CalculationResult):
        """Set and display calculation results"""
        self.current_result = result
        
        if result.success:
            self.display_successful_results(result)
        else:
            self.display_error_results(result)
    
    def display_successful_results(self, result: CalculationResult):
        """Display results from successful calculation"""
        self.status_label.setText("✅ Calculation completed successfully")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        
        # Populate results table
        self.populate_results_table(result.results)
        
        # Show execution info
        exec_time = result.execution_time_ms
        self.execution_label.setText(
            f"Execution time: {exec_time}ms | Module: {result.module_name} | "
            f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Hide error/warning displays
        self.error_text.hide()
        self.warning_text.hide()
        
        # Show warnings if any
        if result.warnings:
            self.warning_text.setPlainText("Warnings:\n" + "\n".join(result.warnings))
            self.warning_text.show()
        
        # Enable buttons
        self.export_button.setEnabled(True)
        self.copy_button.setEnabled(True)
    
    def display_error_results(self, result: CalculationResult):
        """Display error results"""
        self.status_label.setText("❌ Calculation failed")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        # Clear results table
        self.results_table.setRowCount(0)
        
        # Show errors
        if result.errors:
            self.error_text.setPlainText("Errors:\n" + "\n".join(result.errors))
            self.error_text.show()
        
        # Show warnings if any
        if result.warnings:
            self.warning_text.setPlainText("Warnings:\n" + "\n".join(result.warnings))
            self.warning_text.show()
        
        # Show execution info
        exec_time = result.execution_time_ms
        self.execution_label.setText(
            f"Execution time: {exec_time}ms | Module: {result.module_name} | "
            f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Disable buttons
        self.export_button.setEnabled(False)
        self.copy_button.setEnabled(False)
    
    def populate_results_table(self, results: Dict[str, Any]):
        """Populate the results table with calculation results"""
        # Clear existing rows
        self.results_table.setRowCount(0)
        
        # Add result rows
        for key, value in results.items():
            if value is not None:
                row = self.results_table.rowCount()
                self.results_table.insertRow(row)
                
                # Parameter name
                param_item = QTableWidgetItem(self.format_parameter_name(key))
                self.results_table.setItem(row, 0, param_item)
                
                # Value
                value_item = QTableWidgetItem(self.format_value(value))
                self.results_table.setItem(row, 1, value_item)
                
                # Unit
                unit_item = QTableWidgetItem(self.get_unit_for_parameter(key))
                self.results_table.setItem(row, 2, unit_item)
        
        # Resize columns to content
        self.results_table.resizeColumnsToContents()
    
    def format_parameter_name(self, key: str) -> str:
        """Format parameter name for display"""
        # Convert snake_case to Title Case
        formatted = key.replace('_', ' ').title()
        
        # Special formatting for common parameters
        replacements = {
            'Max': 'Maximum',
            'Min': 'Minimum',
            'R1': 'R₁',
            'R2': 'R₂',
            'R3': 'R₃'
        }
        
        for old, new in replacements.items():
            formatted = formatted.replace(old, new)
        
        return formatted
    
    def format_value(self, value: Any) -> str:
        """Format value for display"""
        if isinstance(value, (int, float)):
            if abs(value) >= 1e6 or (abs(value) < 1e-3 and value != 0):
                return f"{value:.3e}"
            else:
                return f"{value:.6g}"
        else:
            return str(value)
    
    def get_unit_for_parameter(self, key: str) -> str:
        """Get unit for parameter"""
        # Common parameter units
        units = {
            'max_deflection': 'm',
            'max_moment': 'N⋅m',
            'max_stress': 'Pa',
            'reaction_left': 'N',
            'reaction_right': 'N',
            'safety_factor': '',
            'total_resistance': 'Ω',
            'total_current': 'A',
            'total_power': 'W',
            'voltage_r1': 'V',
            'voltage_r2': 'V',
            'current_r1': 'A',
            'current_r2': 'A',
            'heat_rate': 'W',
            'thermal_resistance': 'K/W',
            'temperature_gradient': 'K/m',
            'heat_flux': 'W/m²',
            'conduction_rate': 'W',
            'convection_rate': 'W',
            'radiation_rate': 'W'
        }
        
        return units.get(key, '')
    
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        if not self.current_result or not self.current_result.success:
            return
        
        # Create formatted text
        text_lines = [f"Calculation Results - {self.current_result.module_name}"]
        text_lines.append(f"Timestamp: {self.current_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        text_lines.append(f"Execution time: {self.current_result.execution_time_ms}ms")
        text_lines.append("")
        
        for key, value in self.current_result.results.items():
            if value is not None:
                param_name = self.format_parameter_name(key)
                formatted_value = self.format_value(value)
                unit = self.get_unit_for_parameter(key)
                text_lines.append(f"{param_name}: {formatted_value} {unit}")
        
        # Copy to clipboard
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(text_lines))
        
        QMessageBox.information(self, "Copied", "Results copied to clipboard!")
    
    def clear_results(self):
        """Clear all results"""
        self.current_result = None
        self.status_label.setText("No calculation performed")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        self.results_table.setRowCount(0)
        self.execution_label.clear()
        self.error_text.hide()
        self.warning_text.hide()
        self.export_button.setEnabled(False)
        self.copy_button.setEnabled(False)
