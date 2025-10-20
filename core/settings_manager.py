"""
Settings management system for HeroCal.
Handles user preferences, application settings, and configuration.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging


class SettingsManager:
    """Manages application settings and user preferences"""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings: Dict[str, Any] = {}
        self.default_settings = self._get_default_settings()
        self.logger = logging.getLogger(__name__)
        self.load_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default application settings"""
        return {
            "application": {
                "name": "HeroCal",
                "version": "1.0.0",
                "auto_save": True,
                "auto_save_interval": 300,  # 5 minutes
                "check_updates": True,
                "show_tooltips": True,
                "enable_history": True,
                "max_history_items": 100,
                "language": "en"
            },
            "units": {
                "system": "SI",  # SI or Imperial
                "length": "m",
                "force": "N",
                "pressure": "Pa",
                "temperature": "C",
                "energy": "J",
                "power": "W"
            },
            "display": {
                "theme": "dark",  # dark, light, high_contrast
                "font_size": 12,
                "font_family": "Segoe UI",
                "precision": 6,
                "scientific_notation_threshold": 1e-3,
                "show_grid": True,
                "show_legend": True,
                "chart_style": "default"
            },
            "calculation": {
                "max_execution_time": 30,  # seconds
                "enable_caching": True,
                "cache_size": 1000,
                "parallel_calculations": True,
                "max_workers": 4
            },
            "export": {
                "default_format": "PDF",
                "include_charts": True,
                "include_calculations": True,
                "include_metadata": True,
                "chart_resolution": 300,  # DPI
                "page_size": "A4"
            },
            "paths": {
                "projects_directory": "projects",
                "exports_directory": "exports",
                "backups_directory": "backups",
                "temp_directory": "temp"
            },
            "modules": {
                "auto_load_plugins": True,
                "plugin_directory": "modules",
                "enabled_modules": [],
                "disabled_modules": []
            },
            "logging": {
                "level": "INFO",
                "file_logging": True,
                "console_logging": True,
                "log_file": "logs/engicalc.log",
                "max_log_size": 10485760,  # 10MB
                "backup_count": 5
            },
            "webhook": {
                "enabled": True,
                "url": "https://aa50309f1513.ngrok-free.app",
                "timeout": 30,  # seconds
                "retry_attempts": 3,
                "send_calculations": True,
                "send_errors": True,
                "send_project_saves": False
            }
        }
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # Merge with default settings to ensure all keys exist
                self.settings = self._merge_settings(self.default_settings, loaded_settings)
                self.logger.info("Settings loaded successfully")
            else:
                self.settings = self.default_settings.copy()
                self.save_settings()
                self.logger.info("Created default settings file")
                
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
            self.settings = self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Ensure directory exists
            settings_dir = os.path.dirname(self.settings_file)
            if settings_dir and not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Settings saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
            raise
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting value using dot notation (e.g., 'display.theme')"""
        try:
            keys = key.split('.')
            value = self.settings
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.error(f"Failed to get setting {key}: {e}")
            return default
    
    def set_setting(self, key: str, value: Any):
        """Set setting value using dot notation"""
        try:
            keys = key.split('.')
            settings = self.settings
            
            # Navigate to the parent dictionary
            for k in keys[:-1]:
                if k not in settings:
                    settings[k] = {}
                settings = settings[k]
            
            # Set the value
            settings[keys[-1]] = value
            
            self.logger.info(f"Setting {key} updated to {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to set setting {key}: {e}")
            raise
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        try:
            self.settings = self.default_settings.copy()
            self.save_settings()
            self.logger.info("Settings reset to defaults")
            
        except Exception as e:
            self.logger.error(f"Failed to reset settings: {e}")
            raise
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.settings.copy()
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update multiple settings at once"""
        try:
            self.settings = self._merge_settings(self.settings, new_settings)
            self.save_settings()
            self.logger.info("Settings updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update settings: {e}")
            raise
    
    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        """Validate settings structure and values"""
        try:
            # Check required top-level sections
            required_sections = ['application', 'units', 'display', 'calculation']
            for section in required_sections:
                if section not in settings:
                    self.logger.error(f"Missing required section: {section}")
                    return False
            
            # Validate specific values
            if not isinstance(settings['application'].get('auto_save_interval'), int):
                self.logger.error("auto_save_interval must be an integer")
                return False
            
            if settings['display'].get('theme') not in ['dark', 'light', 'high_contrast']:
                self.logger.error("Invalid theme value")
                return False
            
            if settings['units'].get('system') not in ['SI', 'Imperial']:
                self.logger.error("Invalid unit system")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Settings validation failed: {e}")
            return False
    
    def _merge_settings(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded settings with defaults"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Settings exported to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            if self.validate_settings(imported_settings):
                self.settings = self._merge_settings(self.default_settings, imported_settings)
                self.save_settings()
                self.logger.info(f"Settings imported from {file_path}")
                return True
            else:
                self.logger.error("Invalid settings file")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to import settings: {e}")
            return False
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme for current theme"""
        theme = self.get_setting('display.theme', 'dark')
        
        themes = {
            'dark': {
                'background': '#2b2b2b',
                'primary_panel': '#3c3c3c',
                'secondary_panel': '#4a4a4a',
                'text': '#ffffff',
                'accent': '#0078d4',
                'success': '#107c10',
                'warning': '#ff8c00',
                'error': '#d13438'
            },
            'light': {
                'background': '#f5f5f5',
                'primary_panel': '#ffffff',
                'secondary_panel': '#f0f0f0',
                'text': '#323130',
                'accent': '#0078d4',
                'success': '#107c10',
                'warning': '#ff8c00',
                'error': '#d13438'
            },
            'high_contrast': {
                'background': '#000000',
                'primary_panel': '#ffffff',
                'secondary_panel': '#ffffff',
                'text': '#ffffff',
                'accent': '#ffff00',
                'success': '#00ff00',
                'warning': '#ffff00',
                'error': '#ff0000'
            }
        }
        
        return themes.get(theme, themes['dark'])
    
    def get_unit_conversion_factors(self) -> Dict[str, Dict[str, float]]:
        """Get unit conversion factors for current unit system"""
        system = self.get_setting('units.system', 'SI')
        
        if system == 'SI':
            return {
                'length': {'m': 1.0, 'mm': 0.001, 'cm': 0.01, 'km': 1000.0},
                'force': {'N': 1.0, 'kN': 1000.0, 'MN': 1000000.0},
                'pressure': {'Pa': 1.0, 'kPa': 1000.0, 'MPa': 1000000.0, 'GPa': 1000000000.0},
                'temperature': {'C': 1.0, 'K': 1.0, 'F': 1.0}  # Conversion handled separately
            }
        else:  # Imperial
            return {
                'length': {'ft': 1.0, 'in': 1/12, 'yd': 3.0, 'mi': 5280.0},
                'force': {'lbf': 1.0, 'kip': 1000.0, 'ton': 2000.0},
                'pressure': {'psi': 1.0, 'ksi': 1000.0, 'psf': 1/144},
                'temperature': {'F': 1.0, 'R': 1.0, 'C': 1.0}  # Conversion handled separately
            }
