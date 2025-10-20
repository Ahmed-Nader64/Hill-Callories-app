"""
Input panel for HeroCal application.
Provides input forms for calculation modules.
"""

from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QComboBox, QCheckBox, QGroupBox, QGridLayout,
    QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from core.base_module import ModuleInfo, InputField, ValidationResult


class InputPanel(QWidget):
    """Panel for inputting calculation parameters"""
    
    inputs_changed = pyqtSignal(dict)  # Emitted when inputs change
    calculate_requested = pyqtSignal()  # Emitted when calculate button is clicked
    
    def __init__(self):
        super().__init__()
        self.current_module_info: Optional[ModuleInfo] = None
        self.input_widgets: Dict[str, QWidget] = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("Input Parameters")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)
        
        # Scroll area for input fields
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout(self.input_widget)
        
        scroll_area.setWidget(self.input_widget)
        layout.addWidget(scroll_area)
        
        # Button panel
        button_layout = QHBoxLayout()
        
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_requested.emit)
        self.calculate_button.setEnabled(False)
        button_layout.addWidget(self.calculate_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_inputs)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
        # Validation message area
        self.validation_label = QLabel()
        self.validation_label.setWordWrap(True)
        self.validation_label.setStyleSheet("color: red; font-weight: bold;")
        self.validation_label.hide()
        layout.addWidget(self.validation_label)
    
    def set_module(self, module_info: ModuleInfo):
        """Set the current module and create input fields"""
        self.current_module_info = module_info
        self.title_label.setText(f"{module_info.name} - Input Parameters")
        
        # Clear existing inputs
        self.clear_inputs()
        
        # Create input fields
        self.create_input_fields(module_info.input_fields)
        
        # Enable calculate button
        self.calculate_button.setEnabled(True)
        
        # Hide validation message
        self.validation_label.hide()
    
    def create_input_fields(self, input_fields: List[InputField]):
        """Create input fields for the module"""
        for field in input_fields:
            group = QGroupBox(field.label)
            group_layout = QGridLayout(group)
            
            # Create input widget based on field type
            if field.field_type == "number":
                widget = self.create_number_input(field)
            elif field.field_type == "select":
                widget = self.create_select_input(field)
            elif field.field_type == "boolean":
                widget = self.create_boolean_input(field)
            else:
                widget = self.create_text_input(field)
            
            # Store widget reference
            self.input_widgets[field.name] = widget
            
            # Add to layout
            group_layout.addWidget(widget, 0, 0)
            
            # Add description if available
            if field.description:
                desc_label = QLabel(field.description)
                desc_label.setStyleSheet("color: gray; font-size: 10px;")
                desc_label.setWordWrap(True)
                group_layout.addWidget(desc_label, 1, 0)
            
            self.input_layout.addWidget(group)
        
        # Add stretch to push everything to top
        self.input_layout.addStretch()
    
    def create_number_input(self, field: InputField) -> QLineEdit:
        """Create a number input field"""
        line_edit = QLineEdit()
        line_edit.setText(str(field.default_value))
        line_edit.setPlaceholderText(f"Enter {field.label}")
        
        # Add unit label if specified
        if field.unit:
            line_edit.setPlaceholderText(f"Enter {field.label} ({field.unit})")
        
        # Connect change signal
        line_edit.textChanged.connect(self.on_input_changed)
        
        return line_edit
    
    def create_select_input(self, field: InputField) -> QComboBox:
        """Create a select input field"""
        combo = QComboBox()
        
        if field.options:
            combo.addItems(field.options)
        
        # Set default value
        if field.default_value in field.options:
            combo.setCurrentText(field.default_value)
        
        # Connect change signal
        combo.currentTextChanged.connect(self.on_input_changed)
        
        return combo
    
    def create_boolean_input(self, field: InputField) -> QCheckBox:
        """Create a boolean input field"""
        checkbox = QCheckBox()
        checkbox.setChecked(bool(field.default_value))
        
        # Connect change signal
        checkbox.toggled.connect(self.on_input_changed)
        
        return checkbox
    
    def create_text_input(self, field: InputField) -> QLineEdit:
        """Create a text input field"""
        line_edit = QLineEdit()
        line_edit.setText(str(field.default_value))
        line_edit.setPlaceholderText(f"Enter {field.label}")
        
        # Connect change signal
        line_edit.textChanged.connect(self.on_input_changed)
        
        return line_edit
    
    def on_input_changed(self):
        """Handle input changes"""
        inputs = self.get_inputs()
        self.inputs_changed.emit(inputs)
    
    def get_inputs(self) -> Dict[str, Any]:
        """Get current input values"""
        inputs = {}
        
        if not self.current_module_info:
            return inputs
        
        for field in self.current_module_info.input_fields:
            widget = self.input_widgets.get(field.name)
            if widget:
                if field.field_type == "number":
                    try:
                        value = float(widget.text())
                        inputs[field.name] = value
                    except ValueError:
                        inputs[field.name] = None
                elif field.field_type == "select":
                    inputs[field.name] = widget.currentText()
                elif field.field_type == "boolean":
                    inputs[field.name] = widget.isChecked()
                else:
                    inputs[field.name] = widget.text()
        
        return inputs
    
    def update_validation(self, validation_result: ValidationResult):
        """Update validation display"""
        if not validation_result.is_valid:
            error_messages = []
            for field, error in validation_result.errors.items():
                error_messages.append(f"{field}: {error}")
            
            self.validation_label.setText("Validation Errors:\n" + "\n".join(error_messages))
            self.validation_label.setStyleSheet("color: red; font-weight: bold;")
            self.validation_label.show()
            
            # Disable calculate button
            self.calculate_button.setEnabled(False)
        else:
            self.validation_label.hide()
            
            # Enable calculate button if we have a module
            if self.current_module_info:
                self.calculate_button.setEnabled(True)
            
            # Show warnings if any
            if validation_result.warnings:
                warning_messages = []
                for field, warning in validation_result.warnings.items():
                    warning_messages.append(f"{field}: {warning}")
                
                self.validation_label.setText("Warnings:\n" + "\n".join(warning_messages))
                self.validation_label.setStyleSheet("color: orange; font-weight: bold;")
                self.validation_label.show()
    
    def reset_inputs(self):
        """Reset all inputs to default values"""
        if not self.current_module_info:
            return
        
        for field in self.current_module_info.input_fields:
            widget = self.input_widgets.get(field.name)
            if widget:
                if field.field_type == "number":
                    widget.setText(str(field.default_value))
                elif field.field_type == "select":
                    if field.default_value in field.options:
                        widget.setCurrentText(field.default_value)
                elif field.field_type == "boolean":
                    widget.setChecked(bool(field.default_value))
                else:
                    widget.setText(str(field.default_value))
        
        # Clear validation message
        self.validation_label.hide()
        
        # Emit input change
        self.on_input_changed()
    
    def clear_inputs(self):
        """Clear all input fields"""
        # Remove all widgets from layout
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Clear widget references
        self.input_widgets.clear()
        
        # Hide validation message
        self.validation_label.hide()
        
        # Disable calculate button
        self.calculate_button.setEnabled(False)
