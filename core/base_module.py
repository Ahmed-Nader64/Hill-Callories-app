"""
Base module class for all calculation modules in HeroCal.
This provides the interface that all engineering calculation modules must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InputField:
    """Definition of an input field for a calculation module"""
    name: str
    label: str
    field_type: str  # 'number', 'text', 'select', 'boolean'
    default_value: Any
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: Optional[str] = None
    required: bool = True
    description: str = ""
    options: Optional[List[str]] = None  # For select fields


@dataclass
class OutputField:
    """Definition of an output field for a calculation module"""
    name: str
    label: str
    unit: str
    precision: int = 6
    description: str = ""
    format_string: str = ""


@dataclass
class ModuleInfo:
    """Information about a calculation module"""
    name: str
    version: str
    description: str
    category: str
    author: str
    input_fields: List[InputField]
    output_fields: List[OutputField]
    chart_types: List[str]
    dependencies: List[str] = None
    license: str = "MIT"


@dataclass
class CalculationResult:
    """Result of a calculation"""
    success: bool
    results: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    execution_time_ms: int
    module_name: str
    timestamp: datetime
    charts: List[Dict[str, Any]] = None


@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    errors: Dict[str, str]  # field_name -> error_message
    warnings: Dict[str, str]  # field_name -> warning_message
    suggestions: Dict[str, str] = None  # field_name -> suggestion


class BaseModule(ABC):
    """Base class for all calculation modules"""
    
    def __init__(self):
        self.module_info = self.get_info()
        self.is_enabled = True
    
    @abstractmethod
    def get_info(self) -> ModuleInfo:
        """Return module information"""
        pass
    
    @abstractmethod
    def validate_inputs(self, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate input parameters. Return validation result"""
        pass
    
    @abstractmethod
    def calculate(self, inputs: Dict[str, Any]) -> CalculationResult:
        """Perform calculation and return results"""
        pass
    
    @abstractmethod
    def create_chart(self, inputs: Dict[str, Any], results: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create chart data for visualization"""
        pass
    
    def get_input_fields(self) -> List[InputField]:
        """Get list of input fields for this module"""
        return self.module_info.input_fields
    
    def get_output_fields(self) -> List[OutputField]:
        """Get list of output fields for this module"""
        return self.module_info.output_fields
    
    def enable(self):
        """Enable this module"""
        self.is_enabled = True
    
    def disable(self):
        """Disable this module"""
        self.is_enabled = False
    
    def is_module_enabled(self) -> bool:
        """Check if module is enabled"""
        return self.is_enabled
    
    def get_supported_chart_types(self) -> List[str]:
        """Get list of supported chart types"""
        return self.module_info.chart_types
