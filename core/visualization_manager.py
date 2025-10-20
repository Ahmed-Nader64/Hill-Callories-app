"""
Visualization management system for HeroCal.
Handles chart generation, plotting, and visualization export.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import io
import base64
from typing import Dict, Any, List, Optional, Tuple
import logging


class Chart:
    """Represents a chart with data and metadata"""
    
    def __init__(self, chart_type: str, data: Dict[str, Any], options: Dict[str, Any] = None):
        self.chart_id = f"{chart_type}_{id(self)}"
        self.chart_type = chart_type
        self.title = options.get('title', f'{chart_type.title()} Chart') if options else f'{chart_type.title()} Chart'
        self.x_label = options.get('x_label', 'X') if options else 'X'
        self.y_label = options.get('y_label', 'Y') if options else 'Y'
        self.data = data
        self.options = options or {}
        self.created_date = None
        
        # Initialize matplotlib figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
    def update_data(self, new_data: Dict[str, Any]):
        """Update chart data"""
        self.data.update(new_data)
        
    def get_image_data(self, format: str = 'png') -> bytes:
        """Get chart as image data"""
        try:
            buffer = io.BytesIO()
            self.figure.savefig(buffer, format=format, dpi=300, bbox_inches='tight')
            buffer.seek(0)
            return buffer.getvalue()
        except Exception as e:
            logging.error(f"Failed to generate image data: {e}")
            return b""
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize chart to dictionary"""
        return {
            'chart_id': self.chart_id,
            'chart_type': self.chart_type,
            'title': self.title,
            'x_label': self.x_label,
            'y_label': self.y_label,
            'data': self.data,
            'options': self.options,
            'created_date': self.created_date
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Chart':
        """Deserialize chart from dictionary"""
        chart = cls(data['chart_type'], data['data'], data['options'])
        chart.chart_id = data['chart_id']
        chart.title = data['title']
        chart.x_label = data['x_label']
        chart.y_label = data['y_label']
        chart.created_date = data['created_date']
        return chart


class VisualizationManager:
    """Manages chart generation and visualization"""
    
    def __init__(self):
        self.chart_templates = {}
        self.active_charts = {}
        self.logger = logging.getLogger(__name__)
        self._load_chart_templates()
        
        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid' if plt.style.available else 'default')
    
    def _load_chart_templates(self):
        """Load predefined chart templates"""
        self.chart_templates = {
            'line': self._create_line_chart,
            'scatter': self._create_scatter_chart,
            'bar': self._create_bar_chart,
            'histogram': self._create_histogram,
            'deflection_diagram': self._create_deflection_diagram,
            'moment_diagram': self._create_moment_diagram,
            'stress_strain': self._create_stress_strain_chart,
            'circuit_diagram': self._create_circuit_diagram,
            'heat_transfer': self._create_heat_transfer_chart
        }
    
    def create_chart(self, chart_type: str, data: Dict[str, Any], options: Dict[str, Any] = None) -> Chart:
        """Create a chart from data"""
        try:
            if chart_type not in self.chart_templates:
                raise ValueError(f"Unknown chart type: {chart_type}")
            
            chart = Chart(chart_type, data, options)
            chart.created_date = None
            
            # Generate the chart
            self.chart_templates[chart_type](chart)
            
            # Store the chart
            self.active_charts[chart.chart_id] = chart
            
            self.logger.info(f"Created chart: {chart_type}")
            return chart
            
        except Exception as e:
            self.logger.error(f"Failed to create chart {chart_type}: {e}")
            raise
    
    def update_chart(self, chart_id: str, new_data: Dict[str, Any]):
        """Update existing chart with new data"""
        if chart_id in self.active_charts:
            chart = self.active_charts[chart_id]
            chart.update_data(new_data)
            
            # Regenerate the chart
            if chart.chart_type in self.chart_templates:
                self.chart_templates[chart.chart_type](chart)
            
            self.logger.info(f"Updated chart: {chart_id}")
        else:
            self.logger.warning(f"Chart not found: {chart_id}")
    
    def export_chart(self, chart: Chart, format: str, file_path: str) -> bool:
        """Export chart to file"""
        try:
            if format.lower() == 'png':
                chart.figure.savefig(file_path, format='png', dpi=300, bbox_inches='tight')
            elif format.lower() == 'pdf':
                chart.figure.savefig(file_path, format='pdf', bbox_inches='tight')
            elif format.lower() == 'svg':
                chart.figure.savefig(file_path, format='svg', bbox_inches='tight')
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            self.logger.info(f"Exported chart to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export chart: {e}")
            return False
    
    def get_chart_templates(self) -> List[str]:
        """Get list of available chart templates"""
        return list(self.chart_templates.keys())
    
    def clear_charts(self):
        """Clear all active charts"""
        self.active_charts.clear()
        plt.close('all')
        self.logger.info("Cleared all charts")
    
    # Chart template implementations
    def _create_line_chart(self, chart: Chart):
        """Create a line chart"""
        ax = chart.figure.add_subplot(111)
        
        x_data = chart.data.get('x', [])
        y_data = chart.data.get('y', [])
        
        if x_data and y_data:
            ax.plot(x_data, y_data, linewidth=2, marker='o', markersize=4)
        
        ax.set_xlabel(chart.x_label)
        ax.set_ylabel(chart.y_label)
        ax.set_title(chart.title)
        ax.grid(True, alpha=0.3)
        
        chart.figure.tight_layout()
    
    def _create_scatter_chart(self, chart: Chart):
        """Create a scatter chart"""
        ax = chart.figure.add_subplot(111)
        
        x_data = chart.data.get('x', [])
        y_data = chart.data.get('y', [])
        
        if x_data and y_data:
            ax.scatter(x_data, y_data, alpha=0.7, s=50)
        
        ax.set_xlabel(chart.x_label)
        ax.set_ylabel(chart.y_label)
        ax.set_title(chart.title)
        ax.grid(True, alpha=0.3)
        
        chart.figure.tight_layout()
    
    def _create_bar_chart(self, chart: Chart):
        """Create a bar chart"""
        ax = chart.figure.add_subplot(111)
        
        x_data = chart.data.get('x', [])
        y_data = chart.data.get('y', [])
        
        if x_data and y_data:
            ax.bar(x_data, y_data, alpha=0.7)
        
        ax.set_xlabel(chart.x_label)
        ax.set_ylabel(chart.y_label)
        ax.set_title(chart.title)
        ax.grid(True, alpha=0.3, axis='y')
        
        chart.figure.tight_layout()
    
    def _create_histogram(self, chart: Chart):
        """Create a histogram"""
        ax = chart.figure.add_subplot(111)
        
        data = chart.data.get('data', [])
        bins = chart.data.get('bins', 20)
        
        if data:
            ax.hist(data, bins=bins, alpha=0.7, edgecolor='black')
        
        ax.set_xlabel(chart.x_label)
        ax.set_ylabel('Frequency')
        ax.set_title(chart.title)
        ax.grid(True, alpha=0.3, axis='y')
        
        chart.figure.tight_layout()
    
    def _create_deflection_diagram(self, chart: Chart):
        """Create a beam deflection diagram"""
        ax = chart.figure.add_subplot(111)
        
        # Get beam parameters
        length = chart.data.get('length', 5.0)
        x_data = chart.data.get('x', np.linspace(0, length, 100))
        y_data = chart.data.get('y', np.zeros_like(x_data))
        
        # Plot deflection curve
        ax.plot(x_data, y_data, 'b-', linewidth=2, label='Deflection')
        
        # Add beam representation
        ax.axhline(y=0, color='k', linewidth=2, label='Beam')
        
        # Add supports
        support_type = chart.data.get('support_type', 'simply_supported')
        if support_type == 'simply_supported':
            ax.plot(0, 0, '^', markersize=10, color='r', label='Support')
            ax.plot(length, 0, '^', markersize=10, color='r')
        elif support_type == 'cantilever':
            ax.plot(0, 0, '^', markersize=10, color='r', label='Fixed Support')
        
        # Add load
        load_position = chart.data.get('load_position', length/2)
        load_value = chart.data.get('load_value', 1000)
        if load_value > 0:
            ax.arrow(load_position, 0, 0, -0.1, head_width=0.1, head_length=0.05, 
                    fc='g', ec='g', label=f'Load ({load_value} N)')
        
        ax.set_xlabel('Position (m)')
        ax.set_ylabel('Deflection (m)')
        ax.set_title('Beam Deflection Diagram')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlim(-0.1*length, 1.1*length)
        
        chart.figure.tight_layout()
    
    def _create_moment_diagram(self, chart: Chart):
        """Create a moment diagram"""
        ax = chart.figure.add_subplot(111)
        
        x_data = chart.data.get('x', [])
        moment_data = chart.data.get('moment', [])
        
        if x_data and moment_data:
            ax.plot(x_data, moment_data, 'r-', linewidth=2, label='Moment')
            ax.fill_between(x_data, moment_data, alpha=0.3, color='red')
        
        ax.set_xlabel('Position (m)')
        ax.set_ylabel('Moment (N⋅m)')
        ax.set_title('Moment Diagram')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.axhline(y=0, color='k', linewidth=0.5)
        
        chart.figure.tight_layout()
    
    def _create_stress_strain_chart(self, chart: Chart):
        """Create a stress-strain curve"""
        ax = chart.figure.add_subplot(111)
        
        strain_data = chart.data.get('strain', [])
        stress_data = chart.data.get('stress', [])
        
        if strain_data and stress_data:
            ax.plot(strain_data, stress_data, 'b-', linewidth=2, label='Stress-Strain Curve')
            
            # Add yield point if available
            yield_stress = chart.data.get('yield_stress')
            if yield_stress:
                ax.axhline(y=yield_stress, color='r', linestyle='--', label=f'Yield Stress ({yield_stress} Pa)')
        
        ax.set_xlabel('Strain')
        ax.set_ylabel('Stress (Pa)')
        ax.set_title('Stress-Strain Curve')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        chart.figure.tight_layout()
    
    def _create_circuit_diagram(self, chart: Chart):
        """Create a circuit diagram"""
        ax = chart.figure.add_subplot(111)
        
        # Get circuit parameters
        circuit_type = chart.data.get('circuit_type', 'series')
        components = chart.data.get('components', [])
        
        # Draw circuit elements
        if circuit_type == 'series':
            x_positions = np.linspace(0, 5, len(components) + 1)
            for i, component in enumerate(components):
                # Draw resistor
                rect = patches.Rectangle((x_positions[i], -0.5), 0.5, 1, 
                                       linewidth=2, edgecolor='black', facecolor='lightgray')
                ax.add_patch(rect)
                ax.text(x_positions[i] + 0.25, 0, f'R{i+1}', ha='center', va='center')
        
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_title('Circuit Diagram')
        ax.axis('off')
        
        chart.figure.tight_layout()
    
    def _create_heat_transfer_chart(self, chart: Chart):
        """Create a heat transfer chart"""
        ax = chart.figure.add_subplot(111)
        
        x_data = chart.data.get('x', [])
        temp_data = chart.data.get('temperature', [])
        
        if x_data and temp_data:
            ax.plot(x_data, temp_data, 'r-', linewidth=2, label='Temperature')
            ax.fill_between(x_data, temp_data, alpha=0.3, color='red')
        
        ax.set_xlabel('Position (m)')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Temperature Distribution')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        chart.figure.tight_layout()
    
    def create_plotly_chart(self, chart_type: str, data: Dict[str, Any], options: Dict[str, Any] = None) -> go.Figure:
        """Create an interactive Plotly chart"""
        try:
            if chart_type == 'line':
                fig = px.line(x=data.get('x', []), y=data.get('y', []), 
                             title=options.get('title', 'Line Chart') if options else 'Line Chart')
            elif chart_type == 'scatter':
                fig = px.scatter(x=data.get('x', []), y=data.get('y', []), 
                                title=options.get('title', 'Scatter Chart') if options else 'Scatter Chart')
            elif chart_type == 'bar':
                fig = px.bar(x=data.get('x', []), y=data.get('y', []), 
                            title=options.get('title', 'Bar Chart') if options else 'Bar Chart')
            else:
                raise ValueError(f"Unsupported Plotly chart type: {chart_type}")
            
            # Update layout
            if options:
                if 'x_label' in options:
                    fig.update_xaxes(title=options['x_label'])
                if 'y_label' in options:
                    fig.update_yaxes(title=options['y_label'])
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create Plotly chart: {e}")
            raise
    
    def export_plotly_chart(self, fig: go.Figure, format: str, file_path: str) -> bool:
        """Export Plotly chart to file"""
        try:
            if format.lower() == 'html':
                fig.write_html(file_path)
            elif format.lower() == 'png':
                fig.write_image(file_path)
            elif format.lower() == 'pdf':
                fig.write_image(file_path, format='pdf')
            else:
                raise ValueError(f"Unsupported Plotly export format: {format}")
            
            self.logger.info(f"Exported Plotly chart to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export Plotly chart: {e}")
            return False
