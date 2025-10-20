"""
Data management system for HeroCal.
Handles SQLite database operations, project management, and file I/O.
"""

import sqlite3
import json
import os
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging

from .base_module import CalculationResult


class ProjectDatabase:
    """Manages SQLite database for projects and calculations"""
    
    def __init__(self, db_path: str = "database/engicalc.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_database_directory()
        self._init_database()
    
    def _ensure_database_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def _init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Projects table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        modified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        module_type TEXT NOT NULL,
                        file_path TEXT,
                        settings_json TEXT,
                        metadata_json TEXT
                    )
                """)
                
                # Calculations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calculations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_id INTEGER NOT NULL,
                        module_name TEXT NOT NULL,
                        calculation_type TEXT NOT NULL,
                        input_data_json TEXT NOT NULL,
                        results_json TEXT NOT NULL,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        execution_time_ms INTEGER,
                        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                    )
                """)
                
                # Settings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        setting_key TEXT UNIQUE NOT NULL,
                        setting_value TEXT NOT NULL,
                        setting_type TEXT NOT NULL,
                        description TEXT,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Module registry table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS module_registry (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        module_name TEXT UNIQUE NOT NULL,
                        module_version TEXT NOT NULL,
                        module_path TEXT NOT NULL,
                        module_type TEXT NOT NULL,
                        is_enabled BOOLEAN DEFAULT 1,
                        metadata_json TEXT,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Calculation history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS calculation_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_id INTEGER NOT NULL,
                        action_type TEXT NOT NULL,
                        action_data_json TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                    )
                """)
                
                # Create indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculations_project_id ON calculations(project_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculations_module_name ON calculations(module_name)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculations_created_date ON calculations(created_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculation_history_project_id ON calculation_history(project_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculation_history_timestamp ON calculation_history(timestamp)")
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    def create_project(self, name: str, description: str = "", module_type: str = "general") -> int:
        """Create new project and return project ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO projects (name, description, module_type, settings_json, metadata_json)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, module_type, "{}", "{}"))
                
                project_id = cursor.lastrowid
                conn.commit()
                
                self.logger.info(f"Created project: {name} (ID: {project_id})")
                return project_id
                
        except Exception as e:
            self.logger.error(f"Failed to create project: {e}")
            raise
    
    def save_calculation(self, project_id: int, module_name: str, calculation_type: str, 
                        inputs: Dict[str, Any], results: CalculationResult) -> int:
        """Save calculation to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO calculations (project_id, module_name, calculation_type, 
                                            input_data_json, results_json, execution_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    project_id,
                    module_name,
                    calculation_type,
                    json.dumps(inputs),
                    json.dumps({
                        'success': results.success,
                        'results': results.results,
                        'errors': results.errors,
                        'warnings': results.warnings,
                        'charts': results.charts or []
                    }),
                    results.execution_time_ms
                ))
                
                calculation_id = cursor.lastrowid
                
                # Update project modified date
                cursor.execute("""
                    UPDATE projects SET modified_date = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (project_id,))
                
                conn.commit()
                
                self.logger.info(f"Saved calculation for project {project_id}")
                return calculation_id
                
        except Exception as e:
            self.logger.error(f"Failed to save calculation: {e}")
            raise
    
    def load_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Load project from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_date': row[3],
                        'modified_date': row[4],
                        'module_type': row[5],
                        'file_path': row[6],
                        'settings': json.loads(row[7] or '{}'),
                        'metadata': json.loads(row[8] or '{}')
                    }
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to load project {project_id}: {e}")
            return None
    
    def get_calculation_history(self, project_id: int) -> List[Dict[str, Any]]:
        """Get calculation history for project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM calculations 
                    WHERE project_id = ? 
                    ORDER BY created_date DESC
                """, (project_id,))
                
                rows = cursor.fetchall()
                calculations = []
                
                for row in rows:
                    calculations.append({
                        'id': row[0],
                        'project_id': row[1],
                        'module_name': row[2],
                        'calculation_type': row[3],
                        'input_data': json.loads(row[4]),
                        'results': json.loads(row[5]),
                        'created_date': row[6],
                        'execution_time_ms': row[7]
                    })
                
                return calculations
                
        except Exception as e:
            self.logger.error(f"Failed to get calculation history for project {project_id}: {e}")
            return []
    
    def get_recent_projects(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent projects"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM projects 
                    ORDER BY modified_date DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                projects = []
                
                for row in rows:
                    projects.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_date': row[3],
                        'modified_date': row[4],
                        'module_type': row[5],
                        'file_path': row[6],
                        'settings': json.loads(row[7] or '{}'),
                        'metadata': json.loads(row[8] or '{}')
                    })
                
                return projects
                
        except Exception as e:
            self.logger.error(f"Failed to get recent projects: {e}")
            return []
    
    def update_project_metadata(self, project_id: int, metadata: Dict[str, Any]):
        """Update project metadata"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE projects 
                    SET metadata_json = ?, modified_date = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (json.dumps(metadata), project_id))
                
                conn.commit()
                self.logger.info(f"Updated metadata for project {project_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to update project metadata: {e}")
            raise
    
    def delete_project(self, project_id: int) -> bool:
        """Delete project and all associated calculations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
                conn.commit()
                
                self.logger.info(f"Deleted project {project_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to delete project {project_id}: {e}")
            return False


class FileSystemManager:
    """Manages file operations and .ecp project files"""
    
    def __init__(self, project_directory: str = "projects"):
        self.project_directory = project_directory
        self.backup_directory = os.path.join(project_directory, "backups")
        self.logger = logging.getLogger(__name__)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        for directory in [self.project_directory, self.backup_directory]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def save_project_file(self, project_data: Dict[str, Any], file_path: str) -> bool:
        """Save project to .ecp file"""
        try:
            # Create backup if file exists
            if os.path.exists(file_path):
                self.create_backup(file_path)
            
            # Save project data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved project to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save project file {file_path}: {e}")
            return False
    
    def load_project_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load project from .ecp file"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Project file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            self.logger.info(f"Loaded project from {file_path}")
            return project_data
            
        except Exception as e:
            self.logger.error(f"Failed to load project file {file_path}: {e}")
            return None
    
    def create_backup(self, file_path: str) -> str:
        """Create backup of file"""
        try:
            if not os.path.exists(file_path):
                return ""
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            backup_filename = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(self.backup_directory, backup_filename)
            
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return ""
    
    def validate_ecp_file(self, file_path: str) -> bool:
        """Validate .ecp file format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required fields
            required_fields = ['version', 'metadata', 'project_settings']
            for field in required_fields:
                if field not in data:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Invalid .ecp file {file_path}: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            # Implementation for cleaning up temporary files
            pass
        except Exception as e:
            self.logger.error(f"Failed to cleanup temp files: {e}")


class DataManager:
    """Main data management class that coordinates database and file operations"""
    
    def __init__(self, db_path: str = "database/engicalc.db", project_dir: str = "projects"):
        self.database = ProjectDatabase(db_path)
        self.file_manager = FileSystemManager(project_dir)
        self.logger = logging.getLogger(__name__)
    
    def create_project(self, name: str, description: str = "", module_type: str = "general") -> int:
        """Create new project"""
        return self.database.create_project(name, description, module_type)
    
    def save_calculation(self, project_id: int, module_name: str, calculation_type: str, 
                        inputs: Dict[str, Any], results: CalculationResult) -> int:
        """Save calculation to database"""
        return self.database.save_calculation(project_id, module_name, calculation_type, inputs, results)
    
    def load_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Load project from database"""
        return self.database.load_project(project_id)
    
    def get_recent_projects(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent projects"""
        return self.database.get_recent_projects(limit)
    
    def save_project_to_file(self, project_data: Dict[str, Any], file_path: str) -> bool:
        """Save project to .ecp file"""
        return self.file_manager.save_project_file(project_data, file_path)
    
    def load_project_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load project from .ecp file"""
        return self.file_manager.load_project_file(file_path)
