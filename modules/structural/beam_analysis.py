"""
Beam Analysis Module for HeroCal.
Provides structural analysis calculations for various beam configurations.
"""

import numpy as np
from typing import Dict, Any, List
from datetime import datetime

from core.base_module import BaseModule, ModuleInfo, InputField, OutputField, CalculationResult, ValidationResult


class BeamAnalysis(BaseModule):
    """Beam deflection and stress analysis module"""
    
    def __init__(self):
        super().__init__()
    
    def get_info(self) -> ModuleInfo:
        """Return module information"""
        return ModuleInfo(
            name="Beam Analysis",
            version="1.0.0",
            description="Structural analysis of beams with various support conditions",
            category="Structural",
            author="HeroCal Team",
            input_fields=[
                InputField(
                    name="beam_length",
                    label="Beam Length (L)",
                    field_type="number",
                    default_value=5.0,
                    min_value=0.1,
                    max_value=100.0,
                    unit="m",
                    required=True,
                    description="Total length of the beam"
                ),
                InputField(
                    name="applied_load",
                    label="Applied Load (P)",
                    field_type="number",
                    default_value=1000.0,
                    min_value=0.0,
                    max_value=1000000.0,
                    unit="N",
                    required=True,
                    description="Applied point load"
                ),
                InputField(
                    name="moment_of_inertia",
                    label="Moment of Inertia (I)",
                    field_type="number",
                    default_value=0.001,
                    min_value=1e-6,
                    max_value=1.0,
                    unit="m⁴",
                    required=True,
                    description="Second moment of area"
                ),
                InputField(
                    name="modulus_of_elasticity",
                    label="Modulus of Elasticity (E)",
                    field_type="number",
                    default_value=200e9,
                    min_value=1e6,
                    max_value=1e12,
                    unit="Pa",
                    required=True,
                    description="Young's modulus of the material"
                ),
                InputField(
                    name="support_type",
                    label="Support Type",
                    field_type="select",
                    default_value="simply_supported",
                    required=True,
                    description="Type of beam support",
                    options=["simply_supported", "cantilever", "fixed_fixed"]
                ),
                InputField(
                    name="load_position",
                    label="Load Position",
                    field_type="number",
                    default_value=2.5,
                    min_value=0.0,
                    max_value=5.0,
                    unit="m",
                    required=True,
                    description="Position of the applied load from left support"
                ),
                InputField(
                    name="yield_strength",
                    label="Yield Strength",
                    field_type="number",
                    default_value=250e6,
                    min_value=1e6,
                    max_value=2e9,
                    unit="Pa",
                    required=False,
                    description="Material yield strength for safety factor calculation"
                )
            ],
            output_fields=[
                OutputField(
                    name="max_deflection",
                    label="Maximum Deflection",
                    unit="m",
                    precision=6,
                    description="Maximum vertical deflection of the beam"
                ),
                OutputField(
                    name="max_moment",
                    label="Maximum Moment",
                    unit="N⋅m",
                    precision=2,
                    description="Maximum bending moment"
                ),
                OutputField(
                    name="max_stress",
                    label="Maximum Stress",
                    unit="Pa",
                    precision=2,
                    description="Maximum bending stress"
                ),
                OutputField(
                    name="reaction_left",
                    label="Left Reaction",
                    unit="N",
                    precision=2,
                    description="Reaction force at left support"
                ),
                OutputField(
                    name="reaction_right",
                    label="Right Reaction",
                    unit="N",
                    precision=2,
                    description="Reaction force at right support"
                ),
                OutputField(
                    name="safety_factor",
                    label="Safety Factor",
                    unit="",
                    precision=2,
                    description="Factor of safety based on yield strength"
                )
            ],
            chart_types=["deflection_diagram", "moment_diagram", "shear_diagram"],
            dependencies=[],
            license="MIT"
        )
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate input parameters"""
        errors = {}
        warnings = {}
        
        # Check required fields
        required_fields = ['beam_length', 'applied_load', 'moment_of_inertia', 'modulus_of_elasticity', 'support_type', 'load_position']
        for field in required_fields:
            if field not in inputs or inputs[field] is None:
                errors[field] = f"{field} is required"
        
        if errors:
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Validate beam length
        if inputs['beam_length'] <= 0:
            errors['beam_length'] = "Beam length must be positive"
        
        # Validate load position
        if inputs['load_position'] < 0 or inputs['load_position'] > inputs['beam_length']:
            errors['load_position'] = "Load position must be between 0 and beam length"
        
        # Validate applied load
        if inputs['applied_load'] < 0:
            errors['applied_load'] = "Applied load must be non-negative"
        
        # Validate moment of inertia
        if inputs['moment_of_inertia'] <= 0:
            errors['moment_of_inertia'] = "Moment of inertia must be positive"
        
        # Validate modulus of elasticity
        if inputs['modulus_of_elasticity'] <= 0:
            errors['modulus_of_elasticity'] = "Modulus of elasticity must be positive"
        
        # Validate support type
        valid_supports = ["simply_supported", "cantilever", "fixed_fixed"]
        if inputs['support_type'] not in valid_supports:
            errors['support_type'] = f"Support type must be one of: {', '.join(valid_supports)}"
        
        # Warnings
        if inputs['applied_load'] > 100000:
            warnings['applied_load'] = "Very high load - verify material properties"
        
        if inputs['beam_length'] > 50:
            warnings['beam_length'] = "Very long beam - consider lateral stability"
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def calculate(self, inputs: Dict[str, Any]) -> CalculationResult:
        """Perform beam analysis calculation"""
        try:
            # Extract inputs
            L = inputs['beam_length']
            P = inputs['applied_load']
            I = inputs['moment_of_inertia']
            E = inputs['modulus_of_elasticity']
            support_type = inputs['support_type']
            a = inputs['load_position']  # Distance from left support
            b = L - a  # Distance from right support
            
            # Calculate reactions
            if support_type == "simply_supported":
                R_left = P * b / L
                R_right = P * a / L
            elif support_type == "cantilever":
                R_left = P
                R_right = 0
            elif support_type == "fixed_fixed":
                R_left = P * b / L
                R_right = P * a / L
            
            # Calculate maximum moment
            if support_type == "simply_supported":
                M_max = P * a * b / L
            elif support_type == "cantilever":
                M_max = P * a
            elif support_type == "fixed_fixed":
                M_max = P * a * b / L
            
            # Calculate maximum deflection
            if support_type == "simply_supported":
                # Deflection at load point
                delta_max = P * a * b * (L + b) / (6 * E * I * L) if a <= L/2 else P * a * b * (L + a) / (6 * E * I * L)
            elif support_type == "cantilever":
                delta_max = P * a**3 / (3 * E * I)
            elif support_type == "fixed_fixed":
                delta_max = P * a**2 * b**2 / (3 * E * I * L)
            
            # Calculate maximum stress (assuming rectangular cross-section)
            # For rectangular beam: I = b*h^3/12, so h = sqrt(12*I/b)
            # Assuming b = h (square cross-section)
            h = (12 * I)**(1/3)
            c = h / 2  # Distance to extreme fiber
            sigma_max = M_max * c / I
            
            # Calculate safety factor
            safety_factor = None
            if 'yield_strength' in inputs and inputs['yield_strength'] > 0:
                safety_factor = inputs['yield_strength'] / sigma_max
            
            # Prepare results
            results = {
                'max_deflection': delta_max,
                'max_moment': M_max,
                'max_stress': sigma_max,
                'reaction_left': R_left,
                'reaction_right': R_right,
                'safety_factor': safety_factor
            }
            
            # Generate charts
            charts = []
            
            # Deflection diagram
            x = np.linspace(0, L, 100)
            if support_type == "simply_supported":
                y = np.where(x <= a, 
                           P * b * x * (L**2 - x**2 - b**2) / (6 * E * I * L),
                           P * a * (L - x) * (2 * L * x - x**2 - a**2) / (6 * E * I * L))
            elif support_type == "cantilever":
                y = P * x**2 * (3 * a - x) / (6 * E * I)
            elif support_type == "fixed_fixed":
                y = P * a**2 * b**2 / (3 * E * I * L) * (1 - 3 * x / L + 2 * x**2 / L**2)
            
            charts.append({
                'type': 'deflection_diagram',
                'data': {
                    'x': x.tolist(),
                    'y': y.tolist(),
                    'length': L,
                    'support_type': support_type,
                    'load_position': a,
                    'load_value': P
                },
                'title': 'Beam Deflection Diagram',
                'x_label': 'Position (m)',
                'y_label': 'Deflection (m)'
            })
            
            # Moment diagram
            if support_type == "simply_supported":
                M = np.where(x <= a, R_left * x, R_left * x - P * (x - a))
            elif support_type == "cantilever":
                M = P * (a - x)
            elif support_type == "fixed_fixed":
                M = R_left * x - P * np.maximum(0, x - a)
            
            charts.append({
                'type': 'moment_diagram',
                'data': {
                    'x': x.tolist(),
                    'moment': M.tolist()
                },
                'title': 'Moment Diagram',
                'x_label': 'Position (m)',
                'y_label': 'Moment (N⋅m)'
            })
            
            return CalculationResult(
                success=True,
                results=results,
                errors=[],
                warnings=[],
                execution_time_ms=0,  # Will be set by calculation engine
                module_name="Beam Analysis",
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
                module_name="Beam Analysis",
                timestamp=datetime.now()
            )
    
    def create_chart(self, inputs: Dict[str, Any], results: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create chart data for visualization"""
        if chart_type == "deflection_diagram":
            return self._create_deflection_chart(inputs, results)
        elif chart_type == "moment_diagram":
            return self._create_moment_chart(inputs, results)
        elif chart_type == "shear_diagram":
            return self._create_shear_chart(inputs, results)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def _create_deflection_chart(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create deflection diagram data"""
        L = inputs['beam_length']
        P = inputs['applied_load']
        I = inputs['moment_of_inertia']
        E = inputs['modulus_of_elasticity']
        support_type = inputs['support_type']
        a = inputs['load_position']
        
        x = np.linspace(0, L, 100)
        
        if support_type == "simply_supported":
            y = np.where(x <= a, 
                       P * (L - a) * x * (L**2 - x**2 - (L - a)**2) / (6 * E * I * L),
                       P * a * (L - x) * (2 * L * x - x**2 - a**2) / (6 * E * I * L))
        elif support_type == "cantilever":
            y = P * x**2 * (3 * a - x) / (6 * E * I)
        elif support_type == "fixed_fixed":
            y = P * a**2 * (L - a)**2 / (3 * E * I * L) * (1 - 3 * x / L + 2 * x**2 / L**2)
        
        return {
            'type': 'deflection_diagram',
            'data': {
                'x': x.tolist(),
                'y': y.tolist(),
                'length': L,
                'support_type': support_type,
                'load_position': a,
                'load_value': P
            },
            'title': 'Beam Deflection Diagram',
            'x_label': 'Position (m)',
            'y_label': 'Deflection (m)'
        }
    
    def _create_moment_chart(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create moment diagram data"""
        L = inputs['beam_length']
        P = inputs['applied_load']
        support_type = inputs['support_type']
        a = inputs['load_position']
        
        x = np.linspace(0, L, 100)
        R_left = results['reaction_left']
        
        if support_type == "simply_supported":
            M = np.where(x <= a, R_left * x, R_left * x - P * (x - a))
        elif support_type == "cantilever":
            M = P * (a - x)
        elif support_type == "fixed_fixed":
            M = R_left * x - P * np.maximum(0, x - a)
        
        return {
            'type': 'moment_diagram',
            'data': {
                'x': x.tolist(),
                'moment': M.tolist()
            },
            'title': 'Moment Diagram',
            'x_label': 'Position (m)',
            'y_label': 'Moment (N⋅m)'
        }
    
    def _create_shear_chart(self, inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Create shear diagram data"""
        L = inputs['beam_length']
        P = inputs['applied_load']
        support_type = inputs['support_type']
        a = inputs['load_position']
        
        x = np.linspace(0, L, 100)
        R_left = results['reaction_left']
        
        if support_type == "simply_supported":
            V = np.where(x < a, R_left, R_left - P)
        elif support_type == "cantilever":
            V = np.where(x < a, -P, 0)
        elif support_type == "fixed_fixed":
            V = np.where(x < a, R_left, R_left - P)
        
        return {
            'type': 'shear_diagram',
            'data': {
                'x': x.tolist(),
                'shear': V.tolist()
            },
            'title': 'Shear Diagram',
            'x_label': 'Position (m)',
            'y_label': 'Shear Force (N)'
        }
