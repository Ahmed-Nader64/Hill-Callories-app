"""
Core calculation engine for HeroCal.
Manages all calculation modules and provides the main calculation interface.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Type
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future

from .base_module import BaseModule, ModuleInfo, CalculationResult, ValidationResult


class CalculationEngine:
    """Main calculation engine for HeroCal"""
    
    def __init__(self):
        self.modules: Dict[str, BaseModule] = {}
        self.module_registry: Dict[str, ModuleInfo] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.logger = logging.getLogger(__name__)
        
        # Initialize built-in modules
        self._load_builtin_modules()
    
    def register_module(self, module: BaseModule) -> bool:
        """Register a new calculation module"""
        try:
            module_info = module.get_info()
            module_name = module_info.name
            
            if module_name in self.modules:
                self.logger.warning(f"Module {module_name} is already registered. Replacing...")
            
            self.modules[module_name] = module
            self.module_registry[module_name] = module_info
            
            self.logger.info(f"Successfully registered module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register module: {e}")
            return False
    
    def unregister_module(self, module_name: str) -> bool:
        """Unregister a calculation module"""
        try:
            if module_name in self.modules:
                del self.modules[module_name]
                del self.module_registry[module_name]
                self.logger.info(f"Successfully unregistered module: {module_name}")
                return True
            else:
                self.logger.warning(f"Module {module_name} not found for unregistration")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to unregister module {module_name}: {e}")
            return False
    
    def get_available_modules(self) -> List[str]:
        """Get list of available module names"""
        return list(self.modules.keys())
    
    def get_module_info(self, module_name: str) -> Optional[ModuleInfo]:
        """Get information about a specific module"""
        return self.module_registry.get(module_name)
    
    def get_enabled_modules(self) -> List[str]:
        """Get list of enabled module names"""
        return [name for name, module in self.modules.items() if module.is_module_enabled()]
    
    def enable_module(self, module_name: str) -> bool:
        """Enable a module"""
        if module_name in self.modules:
            self.modules[module_name].enable()
            return True
        return False
    
    def disable_module(self, module_name: str) -> bool:
        """Disable a module"""
        if module_name in self.modules:
            self.modules[module_name].disable()
            return True
        return False
    
    def validate_inputs(self, module_name: str, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate inputs for specified module"""
        if module_name not in self.modules:
            return ValidationResult(
                is_valid=False,
                errors={"module": f"Module '{module_name}' not found"},
                warnings={}
            )
        
        try:
            module = self.modules[module_name]
            return module.validate_inputs(inputs)
        except Exception as e:
            self.logger.error(f"Error validating inputs for {module_name}: {e}")
            return ValidationResult(
                is_valid=False,
                errors={"validation": f"Validation error: {str(e)}"},
                warnings={}
            )
    
    def calculate(self, module_name: str, inputs: Dict[str, Any]) -> CalculationResult:
        """Execute calculation for specified module"""
        start_time = time.time()
        
        if module_name not in self.modules:
            return CalculationResult(
                success=False,
                results={},
                errors=[f"Module '{module_name}' not found"],
                warnings=[],
                execution_time_ms=0,
                module_name=module_name,
                timestamp=datetime.now()
            )
        
        try:
            module = self.modules[module_name]
            
            # Validate inputs first
            validation_result = module.validate_inputs(inputs)
            if not validation_result.is_valid:
                return CalculationResult(
                    success=False,
                    results={},
                    errors=[f"Validation failed: {error}" for error in validation_result.errors.values()],
                    warnings=[f"Warning: {warning}" for warning in validation_result.warnings.values()],
                    execution_time_ms=0,
                    module_name=module_name,
                    timestamp=datetime.now()
                )
            
            # Perform calculation
            result = module.calculate(inputs)
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            result.execution_time_ms = execution_time_ms
            
            self.logger.info(f"Calculation completed for {module_name} in {execution_time_ms}ms")
            return result
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            self.logger.error(f"Calculation failed for {module_name}: {e}")
            return CalculationResult(
                success=False,
                results={},
                errors=[f"Calculation error: {str(e)}"],
                warnings=[],
                execution_time_ms=execution_time_ms,
                module_name=module_name,
                timestamp=datetime.now()
            )
    
    def calculate_async(self, module_name: str, inputs: Dict[str, Any]) -> Future:
        """Execute calculation asynchronously"""
        return self.executor.submit(self.calculate, module_name, inputs)
    
    def get_module_categories(self) -> Dict[str, List[str]]:
        """Get modules grouped by category"""
        categories = {}
        for module_name, module_info in self.module_registry.items():
            category = module_info.category
            if category not in categories:
                categories[category] = []
            categories[category].append(module_name)
        return categories
    
    def _load_builtin_modules(self):
        """Load built-in calculation modules"""
        try:
            # Import and register built-in modules
            from modules.structural.beam_analysis import BeamAnalysis
            from modules.electrical.dc_circuit import DCCircuitAnalysis
            from modules.thermal.heat_transfer import HeatTransferAnalysis
            
            # Register modules
            self.register_module(BeamAnalysis())
            self.register_module(DCCircuitAnalysis())
            self.register_module(HeatTransferAnalysis())
            
            self.logger.info("Built-in modules loaded successfully")
            
        except ImportError as e:
            self.logger.warning(f"Could not load some built-in modules: {e}")
        except Exception as e:
            self.logger.error(f"Error loading built-in modules: {e}")
    
    def shutdown(self):
        """Shutdown the calculation engine"""
        self.executor.shutdown(wait=True)
        self.logger.info("Calculation engine shutdown complete")
