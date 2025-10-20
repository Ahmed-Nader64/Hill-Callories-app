"""
Heat Transfer Analysis Module for HeroCal.
Provides thermal analysis calculations for heat transfer problems.
"""

import numpy as np
from typing import Dict, Any, List
from datetime import datetime

from core.base_module import BaseModule, ModuleInfo, InputField, OutputField, CalculationResult, ValidationResult


class HeatTransferAnalysis(BaseModule):
    """Heat transfer analysis module"""
    
    def __init__(self):
        super().__init__()
    
    def get_info(self) -> ModuleInfo:
        """Return module information"""
        return ModuleInfo(
            name="Heat Transfer Analysis",
            version="1.0.0",
            description="Analysis of heat transfer through conduction, convection, and radiation",
            category="Thermal",
            author="HeroCal Team",
            input_fields=[
                InputField(
                    name="heat_transfer_type",
                    label="Heat Transfer Type",
                    field_type="select",
                    default_value="conduction",
                    required=True,
                    description="Type of heat transfer mechanism",
                    options=["conduction", "convection", "radiation", "combined"]
                ),
                InputField(
                    name="thermal_conductivity",
                    label="Thermal Conductivity (k)",
                    field_type="number",
                    default_value=50.0,
                    min_value=0.1,
                    max_value=1000.0,
                    unit="W/m⋅K",
                    required=True,
                    description="Thermal conductivity of the material"
                ),
                InputField(
                    name="thickness",
                    label="Thickness (L)",
                    field_type="number",
                    default_value=0.1,
                    min_value=0.001,
                    max_value=10.0,
                    unit="m",
                    required=True,
                    description="Thickness of the material"
                ),
                InputField(
                    name="area",
                    label="Cross-sectional Area (A)",
                    field_type="number",
                    default_value=1.0,
                    min_value=0.001,
                    max_value=100.0,
                    unit="m²",
                    required=True,
                    description="Cross-sectional area for heat transfer"
                ),
                InputField(
                    name="temp_hot",
                    label="Hot Side Temperature",
                    field_type="number",
                    default_value=100.0,
                    min_value=-273.15,
                    max_value=2000.0,
                    unit="°C",
                    required=True,
                    description="Temperature on the hot side"
                ),
                InputField(
                    name="temp_cold",
                    label="Cold Side Temperature",
                    field_type="number",
                    default_value=20.0,
                    min_value=-273.15,
                    max_value=2000.0,
                    unit="°C",
                    required=True,
                    description="Temperature on the cold side"
                ),
                InputField(
                    name="convection_coefficient",
                    label="Convection Coefficient (h)",
                    field_type="number",
                    default_value=25.0,
                    min_value=1.0,
                    max_value=1000.0,
                    unit="W/m²⋅K",
                    required=False,
                    description="Convection heat transfer coefficient"
                ),
                InputField(
                    name="emissivity",
                    label="Emissivity (ε)",
                    field_type="number",
                    default_value=0.8,
                    min_value=0.0,
                    max_value=1.0,
                    unit="",
                    required=False,
                    description="Surface emissivity for radiation"
                )
            ],
            output_fields=[
                OutputField(
                    name="heat_rate",
                    label="Heat Transfer Rate",
                    unit="W",
                    precision=2,
                    description="Rate of heat transfer"
                ),
                OutputField(
                    name="thermal_resistance",
                    label="Thermal Resistance",
                    unit="K/W",
                    precision=4,
                    description="Thermal resistance of the system"
                ),
                OutputField(
                    name="temperature_gradient",
                    label="Temperature Gradient",
                    unit="K/m",
                    precision=2,
                    description="Temperature gradient through the material"
                ),
                OutputField(
                    name="heat_flux",
                    label="Heat Flux",
                    unit="W/m²",
                    precision=2,
                    description="Heat flux (heat rate per unit area)"
                ),
                OutputField(
                    name="conduction_rate",
                    label="Conduction Rate",
                    unit="W",
                    precision=2,
                    description="Heat transfer rate by conduction"
                ),
                OutputField(
                    name="convection_rate",
                    label="Convection Rate",
                    unit="W",
                    precision=2,
                    description="Heat transfer rate by convection"
                ),
                OutputField(
                    name="radiation_rate",
                    label="Radiation Rate",
                    unit="W",
                    precision=2,
                    description="Heat transfer rate by radiation"
                )
            ],
            chart_types=["temperature_distribution", "heat_flux_diagram", "thermal_resistance"],
            dependencies=[],
            license="MIT"
        )
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate input parameters"""
        errors = {}
        warnings = {}
        
        # Check required fields
        required_fields = ['heat_transfer_type', 'thermal_conductivity', 'thickness', 'area', 'temp_hot', 'temp_cold']
        for field in required_fields:
            if field not in inputs or inputs[field] is None:
                errors[field] = f"{field} is required"
        
        if errors:
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Validate temperatures
        if inputs['temp_hot'] <= inputs['temp_cold']:
            errors['temp_hot'] = "Hot side temperature must be greater than cold side temperature"
        
        if inputs['temp_hot'] < -273.15 or inputs['temp_cold'] < -273.15:
            errors['temp_hot'] = "Temperature cannot be below absolute zero (-273.15°C)"
        
        # Validate material properties
        if inputs['thermal_conductivity'] <= 0:
            errors['thermal_conductivity'] = "Thermal conductivity must be positive"
        
        if inputs['thickness'] <= 0:
            errors['thickness'] = "Thickness must be positive"
        
        if inputs['area'] <= 0:
            errors['area'] = "Area must be positive"
        
        # Validate heat transfer type
        valid_types = ["conduction", "convection", "radiation", "combined"]
        if inputs['heat_transfer_type'] not in valid_types:
            errors['heat_transfer_type'] = f"Heat transfer type must be one of: {', '.join(valid_types)}"
        
        # Validate convection coefficient if needed
        if inputs['heat_transfer_type'] in ['convection', 'combined']:
            if 'convection_coefficient' not in inputs or inputs['convection_coefficient'] is None:
                errors['convection_coefficient'] = "Convection coefficient is required for convection/combined analysis"
            elif inputs['convection_coefficient'] <= 0:
                errors['convection_coefficient'] = "Convection coefficient must be positive"
        
        # Validate emissivity if needed
        if inputs['heat_transfer_type'] in ['radiation', 'combined']:
            if 'emissivity' not in inputs or inputs['emissivity'] is None:
                errors['emissivity'] = "Emissivity is required for radiation/combined analysis"
            elif inputs['emissivity'] < 0 or inputs['emissivity'] > 1:
                errors['emissivity'] = "Emissivity must be between 0 and 1"
        
        # Warnings
        if inputs['temp_hot'] > 1000:
            warnings['temp_hot'] = "Very high temperature - verify material properties"
        
        if inputs['thermal_conductivity'] > 500:
            warnings['thermal_conductivity'] = "Very high thermal conductivity - verify material"
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def calculate(self, inputs: Dict[str, Any]) -> CalculationResult:
        """Perform heat transfer analysis calculation"""
        try:
            # Extract inputs
            heat_type = inputs['heat_transfer_type']
            k = inputs['thermal_conductivity']
            L = inputs['thickness']
            A = inputs['area']
            T_hot = inputs['temp_hot'] + 273.15  # Convert to Kelvin
            T_cold = inputs['temp_cold'] + 273.15  # Convert to Kelvin
            
            # Stefan-Boltzmann constant
            sigma = 5.67e-8  # W/m²⋅K⁴
            
            # Calculate temperature difference
            delta_T = T_hot - T_cold
            
            # Initialize results
            results = {}
            
            # Conduction calculation
            if heat_type in ['conduction', 'combined']:
                R_cond = L / (k * A)  # Thermal resistance for conduction
                Q_cond = delta_T / R_cond  # Heat rate by conduction
                results['conduction_rate'] = Q_cond
                results['thermal_resistance'] = R_cond
            else:
                Q_cond = 0
                R_cond = 0
            
            # Convection calculation
            if heat_type in ['convection', 'combined']:
                h = inputs['convection_coefficient']
                R_conv = 1 / (h * A)  # Thermal resistance for convection
                Q_conv = delta_T / R_conv  # Heat rate by convection
                results['convection_rate'] = Q_conv
                if heat_type == 'convection':
                    results['thermal_resistance'] = R_conv
            else:
                Q_conv = 0
                R_conv = 0
            
            # Radiation calculation
            if heat_type in ['radiation', 'combined']:
                epsilon = inputs['emissivity']
                Q_rad = epsilon * sigma * A * (T_hot**4 - T_cold**4)  # Heat rate by radiation
                results['radiation_rate'] = Q_rad
            else:
                Q_rad = 0
            
            # Total heat transfer rate
            if heat_type == 'conduction':
                Q_total = Q_cond
            elif heat_type == 'convection':
                Q_total = Q_conv
            elif heat_type == 'radiation':
                Q_total = Q_rad
            elif heat_type == 'combined':
                Q_total = Q_cond + Q_conv + Q_rad
                # For combined, use the dominant resistance
                R_total = 1 / (1/R_cond + 1/R_conv) if R_cond > 0 and R_conv > 0 else max(R_cond, R_conv)
                results['thermal_resistance'] = R_total
            
            # Calculate derived quantities
            results['heat_rate'] = Q_total
            results['heat_flux'] = Q_total / A
            results['temperature_gradient'] = delta_T / L
            
            # Generate charts
            charts = []
            
            # Temperature distribution
            x = np.linspace(0, L, 50)
            T_dist = T_cold + (T_hot - T_cold) * (1 - x / L)
            
            charts.append({
                'type': 'temperature_distribution',
                'data': {
                    'x': x.tolist(),
                    'temperature': (np.array(T_dist) - 273.15).tolist()  # Convert back to Celsius
                },
                'title': 'Temperature Distribution',
                'x_label': 'Position (m)',
                'y_label': 'Temperature (°C)'
            })
            
            # Heat flux diagram
            heat_flux_values = [Q_total / A] * len(x)
            charts.append({
                'type': 'heat_flux_diagram',
                'data': {
                    'x': x.tolist(),
                    'heat_flux': heat_flux_values
                },
                'title': 'Heat Flux Distribution',
                'x_label': 'Position (m)',
                'y_label': 'Heat Flux (W/m²)'
            })
            
            return CalculationResult(
                success=True,
                results=results,
                errors=[],
                warnings=[],
                execution_time_ms=0,
                module_name="Heat Transfer Analysis",
                timestamp=datetime.now(),
                charts=charts
            )
            
        except Exception as e:
            return CalculationResult(
                success=False,
                results={},
                errors=[f"Calculation error: {str(e)}"],
                warnings=[],
                execution_time_ms=0,
                module_name="Heat Transfer Analysis",
                timestamp=datetime.now()
            )
    
    def create_chart(self, inputs: Dict[str, Any], results: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create chart data for visualization"""
        if chart_type == "temperature_distribution":
            return self._create_temperature_distribution(inputs, results)
        elif chart_type == "heat_flux_diagram":
            return self._create_heat_flux_diagram(inputs, results)
        elif chart_type == "thermal_resistance":
            return self._create_thermal_resistance_chart(inputs, results)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def _create_temperature_distribution(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create temperature distribution chart data"""
        L = inputs['thickness']
        T_hot = inputs['temp_hot']
        T_cold = inputs['temp_cold']
        
        x = np.linspace(0, L, 50)
        T_dist = T_cold + (T_hot - T_cold) * (1 - x / L)
        
        return {
            'type': 'temperature_distribution',
            'data': {
                'x': x.tolist(),
                'temperature': T_dist.tolist()
            },
            'title': 'Temperature Distribution',
            'x_label': 'Position (m)',
            'y_label': 'Temperature (°C)'
        }
    
    def _create_heat_flux_diagram(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create heat flux diagram data"""
        L = inputs['thickness']
        heat_flux = results['heat_flux']
        
        x = np.linspace(0, L, 50)
        heat_flux_values = [heat_flux] * len(x)
        
        return {
            'type': 'heat_flux_diagram',
            'data': {
                'x': x.tolist(),
                'heat_flux': heat_flux_values
            },
            'title': 'Heat Flux Distribution',
            'x_label': 'Position (m)',
            'y_label': 'Heat Flux (W/m²)'
        }
    
    def _create_thermal_resistance_chart(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create thermal resistance chart data"""
        heat_type = inputs['heat_transfer_type']
        
        if heat_type == 'combined':
            resistances = []
            labels = []
            
            if 'conduction_rate' in results and results['conduction_rate'] > 0:
                resistances.append(1 / results['conduction_rate'] * (inputs['temp_hot'] - inputs['temp_cold']))
                labels.append('Conduction')
            
            if 'convection_rate' in results and results['convection_rate'] > 0:
                resistances.append(1 / results['convection_rate'] * (inputs['temp_hot'] - inputs['temp_cold']))
                labels.append('Convection')
            
            return {
                'type': 'thermal_resistance',
                'data': {
                    'x': labels,
                    'y': resistances
                },
                'title': 'Thermal Resistance Components',
                'x_label': 'Heat Transfer Mode',
                'y_label': 'Thermal Resistance (K/W)'
            }
        else:
            return {
                'type': 'thermal_resistance',
                'data': {
                    'x': [heat_type.title()],
                    'y': [results['thermal_resistance']]
                },
                'title': 'Thermal Resistance',
                'x_label': 'Heat Transfer Mode',
                'y_label': 'Thermal Resistance (K/W)'
            }
