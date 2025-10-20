"""
DC Circuit Analysis Module for HeroCal.
Provides electrical circuit analysis for DC circuits.
"""

import numpy as np
from typing import Dict, Any, List
from datetime import datetime

from core.base_module import BaseModule, ModuleInfo, InputField, OutputField, CalculationResult, ValidationResult


class DCCircuitAnalysis(BaseModule):
    """DC circuit analysis module"""
    
    def __init__(self):
        super().__init__()
    
    def get_info(self) -> ModuleInfo:
        """Return module information"""
        return ModuleInfo(
            name="DC Circuit Analysis",
            version="1.0.0",
            description="Analysis of DC electrical circuits with series and parallel components",
            category="Electrical",
            author="HeroCal Team",
            input_fields=[
                InputField(
                    name="circuit_type",
                    label="Circuit Type",
                    field_type="select",
                    default_value="series",
                    required=True,
                    description="Type of circuit configuration",
                    options=["series", "parallel", "mixed"]
                ),
                InputField(
                    name="voltage_source",
                    label="Voltage Source (V)",
                    field_type="number",
                    default_value=12.0,
                    min_value=0.0,
                    max_value=1000.0,
                    unit="V",
                    required=True,
                    description="Source voltage"
                ),
                InputField(
                    name="resistance_1",
                    label="Resistance 1 (R1)",
                    field_type="number",
                    default_value=10.0,
                    min_value=0.1,
                    max_value=10000.0,
                    unit="Ω",
                    required=True,
                    description="First resistance value"
                ),
                InputField(
                    name="resistance_2",
                    label="Resistance 2 (R2)",
                    field_type="number",
                    default_value=20.0,
                    min_value=0.1,
                    max_value=10000.0,
                    unit="Ω",
                    required=True,
                    description="Second resistance value"
                ),
                InputField(
                    name="resistance_3",
                    label="Resistance 3 (R3)",
                    field_type="number",
                    default_value=0.0,
                    min_value=0.0,
                    max_value=10000.0,
                    unit="Ω",
                    required=False,
                    description="Third resistance value (optional)"
                )
            ],
            output_fields=[
                OutputField(
                    name="total_resistance",
                    label="Total Resistance",
                    unit="Ω",
                    precision=2,
                    description="Equivalent resistance of the circuit"
                ),
                OutputField(
                    name="total_current",
                    label="Total Current",
                    unit="A",
                    precision=4,
                    description="Total current in the circuit"
                ),
                OutputField(
                    name="total_power",
                    label="Total Power",
                    unit="W",
                    precision=2,
                    description="Total power dissipated"
                ),
                OutputField(
                    name="voltage_r1",
                    label="Voltage across R1",
                    unit="V",
                    precision=2,
                    description="Voltage drop across first resistor"
                ),
                OutputField(
                    name="voltage_r2",
                    label="Voltage across R2",
                    unit="V",
                    precision=2,
                    description="Voltage drop across second resistor"
                ),
                OutputField(
                    name="current_r1",
                    label="Current through R1",
                    unit="A",
                    precision=4,
                    description="Current through first resistor"
                ),
                OutputField(
                    name="current_r2",
                    label="Current through R2",
                    unit="A",
                    precision=4,
                    description="Current through second resistor"
                )
            ],
            chart_types=["circuit_diagram", "voltage_distribution", "power_distribution"],
            dependencies=[],
            license="MIT"
        )
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate input parameters"""
        errors = {}
        warnings = {}
        
        # Check required fields
        required_fields = ['circuit_type', 'voltage_source', 'resistance_1', 'resistance_2']
        for field in required_fields:
            if field not in inputs or inputs[field] is None:
                errors[field] = f"{field} is required"
        
        if errors:
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Validate voltage source
        if inputs['voltage_source'] <= 0:
            errors['voltage_source'] = "Voltage source must be positive"
        
        # Validate resistances
        for i in range(1, 4):
            field = f'resistance_{i}'
            if field in inputs and inputs[field] is not None:
                if inputs[field] < 0:
                    errors[field] = f"Resistance {i} must be non-negative"
                elif inputs[field] == 0 and i <= 2:
                    errors[field] = f"Resistance {i} cannot be zero"
        
        # Validate circuit type
        valid_types = ["series", "parallel", "mixed"]
        if inputs['circuit_type'] not in valid_types:
            errors['circuit_type'] = f"Circuit type must be one of: {', '.join(valid_types)}"
        
        # Warnings
        if inputs['voltage_source'] > 100:
            warnings['voltage_source'] = "High voltage - ensure proper safety measures"
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def calculate(self, inputs: Dict[str, Any]) -> CalculationResult:
        """Perform DC circuit analysis calculation"""
        try:
            # Extract inputs
            circuit_type = inputs['circuit_type']
            V_source = inputs['voltage_source']
            R1 = inputs['resistance_1']
            R2 = inputs['resistance_2']
            R3 = inputs.get('resistance_3', 0)
            
            # Calculate equivalent resistance
            if circuit_type == "series":
                R_total = R1 + R2 + R3
            elif circuit_type == "parallel":
                if R3 > 0:
                    R_total = 1 / (1/R1 + 1/R2 + 1/R3)
                else:
                    R_total = 1 / (1/R1 + 1/R2)
            elif circuit_type == "mixed":
                # R1 and R2 in parallel, then in series with R3
                R_parallel = 1 / (1/R1 + 1/R2)
                R_total = R_parallel + R3 if R3 > 0 else R_parallel
            
            # Calculate total current
            I_total = V_source / R_total
            
            # Calculate voltages and currents for each resistor
            if circuit_type == "series":
                I1 = I2 = I3 = I_total
                V1 = I1 * R1
                V2 = I2 * R2
                V3 = I3 * R3 if R3 > 0 else 0
            elif circuit_type == "parallel":
                V1 = V2 = V3 = V_source
                I1 = V1 / R1
                I2 = V2 / R2
                I3 = V3 / R3 if R3 > 0 else 0
            elif circuit_type == "mixed":
                # R1 and R2 in parallel, then in series with R3
                V_parallel = I_total * (1 / (1/R1 + 1/R2))
                V1 = V2 = V_parallel
                V3 = I_total * R3 if R3 > 0 else 0
                I1 = V1 / R1
                I2 = V2 / R2
                I3 = I_total
            
            # Calculate power
            P_total = V_source * I_total
            P1 = V1 * I1
            P2 = V2 * I2
            P3 = V3 * I3 if R3 > 0 else 0
            
            # Prepare results
            results = {
                'total_resistance': R_total,
                'total_current': I_total,
                'total_power': P_total,
                'voltage_r1': V1,
                'voltage_r2': V2,
                'current_r1': I1,
                'current_r2': I2
            }
            
            if R3 > 0:
                results['voltage_r3'] = V3
                results['current_r3'] = I3
                results['power_r1'] = P1
                results['power_r2'] = P2
                results['power_r3'] = P3
            
            # Generate charts
            charts = []
            
            # Circuit diagram
            charts.append({
                'type': 'circuit_diagram',
                'data': {
                    'circuit_type': circuit_type,
                    'components': [
                        {'type': 'voltage_source', 'value': V_source, 'unit': 'V'},
                        {'type': 'resistor', 'value': R1, 'unit': 'Ω', 'name': 'R1'},
                        {'type': 'resistor', 'value': R2, 'unit': 'Ω', 'name': 'R2'}
                    ]
                },
                'title': 'Circuit Diagram',
                'x_label': '',
                'y_label': ''
            })
            
            # Voltage distribution
            if circuit_type == "series":
                voltages = [V1, V2, V3] if R3 > 0 else [V1, V2]
                resistors = ['R1', 'R2', 'R3'] if R3 > 0 else ['R1', 'R2']
            else:
                voltages = [V1, V2, V3] if R3 > 0 else [V1, V2]
                resistors = ['R1', 'R2', 'R3'] if R3 > 0 else ['R1', 'R2']
            
            charts.append({
                'type': 'voltage_distribution',
                'data': {
                    'x': resistors,
                    'y': voltages
                },
                'title': 'Voltage Distribution',
                'x_label': 'Resistor',
                'y_label': 'Voltage (V)'
            })
            
            return CalculationResult(
                success=True,
                results=results,
                errors=[],
                warnings=[],
                execution_time_ms=0,
                module_name="DC Circuit Analysis",
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
                module_name="DC Circuit Analysis",
                timestamp=datetime.now()
            )
    
    def create_chart(self, inputs: Dict[str, Any], results: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create chart data for visualization"""
        if chart_type == "circuit_diagram":
            return self._create_circuit_diagram(inputs, results)
        elif chart_type == "voltage_distribution":
            return self._create_voltage_distribution(inputs, results)
        elif chart_type == "power_distribution":
            return self._create_power_distribution(inputs, results)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def _create_circuit_diagram(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create circuit diagram data"""
        return {
            'type': 'circuit_diagram',
            'data': {
                'circuit_type': inputs['circuit_type'],
                'components': [
                    {'type': 'voltage_source', 'value': inputs['voltage_source'], 'unit': 'V'},
                    {'type': 'resistor', 'value': inputs['resistance_1'], 'unit': 'Ω', 'name': 'R1'},
                    {'type': 'resistor', 'value': inputs['resistance_2'], 'unit': 'Ω', 'name': 'R2'}
                ]
            },
            'title': 'Circuit Diagram',
            'x_label': '',
            'y_label': ''
        }
    
    def _create_voltage_distribution(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create voltage distribution chart data"""
        R3 = inputs.get('resistance_3', 0)
        
        if R3 > 0:
            voltages = [results['voltage_r1'], results['voltage_r2'], results['voltage_r3']]
            resistors = ['R1', 'R2', 'R3']
        else:
            voltages = [results['voltage_r1'], results['voltage_r2']]
            resistors = ['R1', 'R2']
        
        return {
            'type': 'voltage_distribution',
            'data': {
                'x': resistors,
                'y': voltages
            },
            'title': 'Voltage Distribution',
            'x_label': 'Resistor',
            'y_label': 'Voltage (V)'
        }
    
    def _create_power_distribution(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create power distribution chart data"""
        R3 = inputs.get('resistance_3', 0)
        
        if R3 > 0:
            powers = [results['power_r1'], results['power_r2'], results['power_r3']]
            resistors = ['R1', 'R2', 'R3']
        else:
            powers = [results['power_r1'], results['power_r2']]
            resistors = ['R1', 'R2']
        
        return {
            'type': 'power_distribution',
            'data': {
                'x': resistors,
                'y': powers
            },
            'title': 'Power Distribution',
            'x_label': 'Resistor',
            'y_label': 'Power (W)'
        }
