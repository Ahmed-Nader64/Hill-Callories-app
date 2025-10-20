"""
Visualization panel for HeroCal application.
Displays charts and graphs for calculation results.
"""

from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTabWidget, QScrollArea, QFrame, QMessageBox, QComboBox,
    QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.visualization_manager import VisualizationManager, Chart


class VisualizationPanel(QWidget):
    """Panel for displaying charts and visualizations"""
    
    def __init__(self, visualization_manager: VisualizationManager):
        super().__init__()
        self.visualization_manager = visualization_manager
        self.current_charts: List[Chart] = []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Visualization")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Chart tabs
        self.chart_tabs = QTabWidget()
        self.chart_tabs.setTabPosition(QTabWidget.TabPosition.North)
        layout.addWidget(self.chart_tabs)
        
        # Control panel
        control_group = QGroupBox("Chart Controls")
        control_layout = QGridLayout(control_group)
        
        # Export format selector
        control_layout.addWidget(QLabel("Export Format:"), 0, 0)
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["PNG", "PDF", "SVG"])
        control_layout.addWidget(self.export_format_combo, 0, 1)
        
        # Export button
        self.export_button = QPushButton("Export Chart")
        self.export_button.clicked.connect(self.export_current_chart)
        self.export_button.setEnabled(False)
        control_layout.addWidget(self.export_button, 0, 2)
        
        # Clear button
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_charts)
        control_layout.addWidget(self.clear_button, 1, 0)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_charts)
        control_layout.addWidget(self.refresh_button, 1, 1)
        
        layout.addWidget(control_group)
        
        # Status label
        self.status_label = QLabel("No charts to display")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def add_chart(self, chart: Chart):
        """Add a new chart to the visualization panel"""
        self.current_charts.append(chart)
        
        # Create scroll area for the chart
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Add the chart canvas to scroll area
        scroll_area.setWidget(chart.canvas)
        
        # Add tab
        tab_name = chart.title if chart.title else f"Chart {len(self.current_charts)}"
        self.chart_tabs.addTab(scroll_area, tab_name)
        
        # Update status
        self.status_label.setText(f"Displaying {len(self.current_charts)} chart(s)")
        self.status_label.setStyleSheet("color: green;")
        
        # Enable export button
        self.export_button.setEnabled(True)
    
    def remove_chart(self, chart_id: str):
        """Remove a chart from the visualization panel"""
        for i, chart in enumerate(self.current_charts):
            if chart.chart_id == chart_id:
                # Remove from list
                self.current_charts.pop(i)
                
                # Remove tab
                self.chart_tabs.removeTab(i)
                
                # Update status
                if self.current_charts:
                    self.status_label.setText(f"Displaying {len(self.current_charts)} chart(s)")
                else:
                    self.status_label.setText("No charts to display")
                    self.status_label.setStyleSheet("color: gray; font-style: italic;")
                    self.export_button.setEnabled(False)
                
                break
    
    def clear_charts(self):
        """Clear all charts"""
        self.current_charts.clear()
        self.chart_tabs.clear()
        self.status_label.setText("No charts to display")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        self.export_button.setEnabled(False)
        
        # Clear visualization manager
        self.visualization_manager.clear_charts()
    
    def refresh_charts(self):
        """Refresh all charts"""
        if not self.current_charts:
            return
        
        # Clear and redraw all charts
        for chart in self.current_charts:
            chart.canvas.draw()
        
        self.status_label.setText(f"Refreshed {len(self.current_charts)} chart(s)")
    
    def export_current_chart(self):
        """Export the currently selected chart"""
        current_index = self.chart_tabs.currentIndex()
        if current_index < 0 or current_index >= len(self.current_charts):
            QMessageBox.warning(self, "No Chart Selected", "Please select a chart to export.")
            return
        
        chart = self.current_charts[current_index]
        format_type = self.export_format_combo.currentText().lower()
        
        # Get file path from user
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            f"Export Chart as {format_type.upper()}", 
            f"{chart.title}.{format_type}", 
            f"{format_type.upper()} Files (*.{format_type});;All Files (*)"
        )
        
        if file_path:
            success = self.visualization_manager.export_chart(chart, format_type, file_path)
            if success:
                QMessageBox.information(self, "Export Successful", f"Chart exported to {file_path}")
            else:
                QMessageBox.critical(self, "Export Failed", "Failed to export chart.")
    
    def get_chart_info(self) -> List[Dict[str, Any]]:
        """Get information about all current charts"""
        chart_info = []
        for chart in self.current_charts:
            chart_info.append({
                'id': chart.chart_id,
                'type': chart.chart_type,
                'title': chart.title,
                'created_date': chart.created_date
            })
        return chart_info
    
    def set_chart_theme(self, theme: str):
        """Set theme for all charts"""
        # This would update the matplotlib style for all charts
        # Implementation depends on the specific charting library used
        pass
