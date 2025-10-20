# System Design Summary

## HeroCal - Engineering Calculator Application

**Version:** 1.0  
**Date:** December 2024  
**Author:** HeroCal Development Team

---

## 🎯 **PHASE 2 — SYSTEM DESIGN COMPLETE**

### ✅ **Deliverable: System Design Document (with UML diagrams + GUI mockups)**

---

## 📋 **Design Overview**

### **Architecture Pattern: 3-Tier Layered Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                PRESENTATION LAYER (GUI)                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  PyQt6 + QML + CSS Styling                             │ │
│  │  • MainWindow                                          │ │
│  │  • Module Dialogs                                      │ │
│  │  • Visualization Widgets                               │ │
│  │  • Settings Interface                                  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 LOGIC LAYER (SERVICES)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Python Classes & Services                             │ │
│  │  • CalculationEngine                                   │ │
│  │  • VisualizationManager                                │ │
│  │  • ModuleManager                                       │ │
│  │  • ValidationService                                   │ │
│  │  • ExportService                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 DATA LAYER (STORAGE)                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  SQLite / JSON / ConfigParser                          │ │
│  │  • ProjectDatabase                                     │ │
│  │  • SettingsManager                                     │ │
│  │  • FileSystemManager                                   │ │
│  │  • CacheManager                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ **Key Components Designed**

### **1. Core Application Classes**

| Component                | Responsibility               | Key Methods                                              |
| ------------------------ | ---------------------------- | -------------------------------------------------------- |
| **MainWindow**           | Main application interface   | `open_project()`, `save_project()`, `show_results()`     |
| **CalculationEngine**    | Core calculation processing  | `calculate()`, `validate_inputs()`, `register_module()`  |
| **ModuleManager**        | Plugin system management     | `load_module()`, `unload_module()`, `get_module_info()`  |
| **ProjectManager**       | Project lifecycle management | `create_project()`, `load_project()`, `export_project()` |
| **VisualizationManager** | Chart and graph generation   | `create_chart()`, `export_chart()`, `update_chart()`     |

### **2. Engineering Modules**

| Module Type    | Components                                          | Key Calculations                                |
| -------------- | --------------------------------------------------- | ----------------------------------------------- |
| **Structural** | BeamAnalysis, StressAnalysis, ColumnAnalysis        | Deflection, stress, moment calculations         |
| **Electrical** | DCCircuitAnalysis, ACCircuitAnalysis, PowerAnalysis | Ohm's law, power, impedance calculations        |
| **Thermal**    | HeatTransferAnalysis, IdealGasLawAnalysis           | Heat transfer, gas law, efficiency calculations |
| **Custom**     | Plugin system for extensibility                     | User-defined calculation modules                |

### **3. Data Management**

| Component             | Purpose                    | Key Features                             |
| --------------------- | -------------------------- | ---------------------------------------- |
| **ProjectDatabase**   | SQLite database management | Projects, calculations, settings storage |
| **FileSystemManager** | .ecp file operations       | Save/load projects, export formats       |
| **SettingsManager**   | User preferences           | Units, themes, precision control         |
| **CacheManager**      | Performance optimization   | Calculation result caching               |

---

## 📊 **Database Schema**

### **Core Tables**

```sql
-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    module_type TEXT NOT NULL,
    file_path TEXT,
    settings_json TEXT,
    metadata_json TEXT
);

-- Calculations table
CREATE TABLE calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    module_name TEXT NOT NULL,
    calculation_type TEXT NOT NULL,
    input_data_json TEXT NOT NULL,
    results_json TEXT NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Settings table
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type TEXT NOT NULL,
    description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Module registry table
CREATE TABLE module_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT UNIQUE NOT NULL,
    module_version TEXT NOT NULL,
    module_path TEXT NOT NULL,
    module_type TEXT NOT NULL,
    is_enabled BOOLEAN DEFAULT 1,
    metadata_json TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 **User Interface Design**

### **Main Window Layout**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File  Edit  View  Modules  Settings  Help                                    [Min] [Max] [X] │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [New] [Open] [Save] [Export] [Undo] [Redo] [Print]    [Units: SI ▼] [Theme: Dark ▼] [Help] │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────────────────────────────────────────────────┐ ┌─────────────────┐ │
│ │   MODULES   │ │                    INPUT PANEL                          │ │  VISUALIZATION  │ │
│ │             │ │                                                         │ │                 │ │
│ │ 📐 Structural│ │  ┌─────────────────────────────────────────────────────┐ │ │  ┌─────────────┐ │ │
│ │   • Beam    │ │  │ Beam Analysis Calculator                            │ │ │  │    Chart    │ │ │
│ │   • Column  │ │  │                                                     │ │ │  │             │ │ │
│ │   • Frame   │ │  │ Beam Length (L):     [5.0        ] m               │ │ │  │             │ │ │
│ │             │ │  │ Applied Load (P):    [1000       ] N               │ │ │  │             │ │ │
│ │ ⚡ Electrical│ │  │ Moment of Inertia:   [0.001      ] m⁴              │ │ │  │             │ │ │
│ │   • DC      │ │  │ Modulus of Elasticity:[2e11       ] Pa              │ │ │  │             │ │ │
│ │   • AC      │ │  │ Support Type:        [Simply ▼   ]                 │ │ │  │             │ │ │
│ │             │ │  │ Load Position:       [2.5        ] m               │ │ │  │             │ │ │
│ │ 🔥 Thermal  │ │  │                                                     │ │ │  │             │ │ │
│ │   • Heat    │ │  │ [Calculate] [Reset] [Export] [Show Chart]          │ │ │  │             │ │ │
│ │   • Gas     │ │  └─────────────────────────────────────────────────────┘ │ │  └─────────────┘ │ │
│ │             │ │                                                         │ │                 │ │
│ │ 🔧 Custom   │ │  ┌─────────────────────────────────────────────────────┐ │ │  Results:        │ │
│ │   • Plugin1 │ │  │ Results                                             │ │ │  Max Deflection: │ │
│ │   • Plugin2 │ │  │ ┌─────────────────────────────────────────────────┐ │ │ │  1.56 mm         │ │
│ │             │ │  │ │ Maximum Deflection:   1.56 mm                  │ │ │ │  Max Stress:     │ │
│ │ 📊 Recent   │ │  │ │ Maximum Stress:       1.25 MPa                 │ │ │ │  1.25 MPa        │ │
│ │   • Proj1   │ │  │ │ Left Reaction:        500 N                    │ │ │ │  Safety Factor:  │ │
│ │   • Proj2   │ │  │ │ Right Reaction:       500 N                    │ │ │ │  2.4             │ │
│ │   • Proj3   │ │  │ │ Safety Factor:        2.4                      │ │ │ │                 │ │
│ │             │ │  │ └─────────────────────────────────────────────────┘ │ │ │                 │ │
│ └─────────────┘ └─────────────────────────────────────────────────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Project: Beam Analysis.ecp | Last Saved: 14:45 | Auto-save: ON | Ready | Memory: 0.0 | [M+] [M-] [MR] [MC] │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### **Theme Support**

| Theme             | Background | Primary Panel | Text    | Accent  |
| ----------------- | ---------- | ------------- | ------- | ------- |
| **Dark**          | #2b2b2b    | #3c3c3c       | #ffffff | #0078d4 |
| **Light**         | #f5f5f5    | #ffffff       | #323130 | #0078d4 |
| **High Contrast** | #000000    | #ffffff       | #ffffff | #ffff00 |

---

## 🔄 **Process Flows**

### **Main Calculation Flow**

```
User Input → Input Validation → Module Selection → Calculation Engine →
Result Processing → Visualization Generation → Result Display → Auto-save
```

### **Project Management Flow**

```
New Project → Project Creation Dialog → Database Storage → UI Update →
Ready for Calculations
```

### **Module Loading Flow**

```
Application Startup → Scan Built-in Modules → Load Plugin Modules →
Register Modules → Update UI Module List → Ready for Use
```

---

## 📁 **File Format Specifications**

### **.ecp (Engineering Calculator Project) Format**

```json
{
  "version": "1.0",
  "metadata": {
    "name": "Beam Analysis Project",
    "description": "Structural analysis of simply supported beam",
    "created": "2024-12-15T10:30:00Z",
    "modified": "2024-12-15T14:45:00Z",
    "author": "John Engineer",
    "tags": ["structural", "beam", "deflection"]
  },
  "project_settings": {
    "units": "SI",
    "precision": 6,
    "theme": "dark",
    "auto_save": true,
    "auto_save_interval": 300
  },
  "modules": {
    "structural": {
      "beam_analysis": {
        "inputs": {
          "beam_length": 5.0,
          "applied_load": 1000.0,
          "moment_of_inertia": 0.001,
          "modulus_of_elasticity": 200000000000.0,
          "support_type": "simply_supported",
          "load_position": 2.5
        },
        "results": {
          "max_deflection": 0.0015625,
          "max_stress": 1250000.0,
          "reaction_force_left": 500.0,
          "reaction_force_right": 500.0,
          "safety_factor": 2.4
        },
        "charts": [
          {
            "type": "deflection_diagram",
            "data": {
              "x": [0, 1, 2, 3, 4, 5],
              "y": [0, 0.0005, 0.001, 0.00125, 0.001, 0]
            },
            "title": "Beam Deflection Diagram",
            "x_label": "Position (m)",
            "y_label": "Deflection (m)"
          }
        ]
      }
    }
  }
}
```

---

## 🔧 **API Specifications**

### **Module Interface**

```python
class BaseModule(ABC):
    """Base class for all calculation modules"""

    @abstractmethod
    def get_info(self) -> ModuleInfo:
        """Return module information"""
        pass

    @abstractmethod
    def validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Validate input parameters. Return dict of errors (empty if valid)"""
        pass

    @abstractmethod
    def calculate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Perform calculation and return results"""
        pass

    @abstractmethod
    def create_chart(self, inputs: Dict[str, Any], results: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create chart data for visualization"""
        pass
```

### **Calculation Engine API**

```python
class CalculationEngine:
    """Main calculation engine interface"""

    def register_module(self, module: BaseModule) -> bool:
        """Register a new calculation module"""
        pass

    def calculate(self, module_name: str, inputs: Dict[str, Any]) -> CalculationResult:
        """Execute calculation for specified module"""
        pass

    def validate_inputs(self, module_name: str, inputs: Dict[str, Any]) -> ValidationResult:
        """Validate inputs for specified module"""
        pass
```

---

## ⚡ **Performance Specifications**

### **Performance Targets**

| Metric                    | Target      | Measurement                   |
| ------------------------- | ----------- | ----------------------------- |
| **Application Startup**   | < 3 seconds | Time from launch to ready     |
| **Calculation Execution** | < 1 second  | Per calculation               |
| **UI Response Time**      | < 100ms     | User input to visual feedback |
| **Chart Generation**      | < 500ms     | Per chart                     |
| **File I/O Operations**   | < 2 seconds | Project save/load             |
| **Memory Usage**          | < 500MB     | During normal operation       |

### **Optimization Strategies**

1. **Lazy Loading**: Load modules only when needed
2. **Caching**: Cache calculation results and chart data
3. **Background Processing**: Perform calculations in separate threads
4. **Database Indexing**: Optimize database queries with proper indexes
5. **Memory Management**: Implement proper cleanup and garbage collection

---

## 🛡️ **Security and Error Handling**

### **Security Measures**

1. **Local Storage**: All data stored locally on user's machine
2. **Input Sanitization**: Validate and sanitize all user inputs
3. **File Validation**: Validate .ecp files before loading
4. **Module Sandboxing**: Isolate plugin modules for security

### **Error Handling Strategy**

1. **Input Validation Errors**: User-friendly messages with correction suggestions
2. **Calculation Errors**: Graceful handling with recovery options
3. **System Errors**: Comprehensive logging and user notification
4. **File I/O Errors**: Automatic backup and recovery mechanisms

---

## 🧪 **Testing Strategy**

### **Testing Levels**

| Level                   | Scope                   | Tools                  | Coverage      |
| ----------------------- | ----------------------- | ---------------------- | ------------- |
| **Unit Testing**        | Individual components   | pytest, unittest       | 90%+          |
| **Integration Testing** | Component interactions  | pytest, mock           | 80%+          |
| **System Testing**      | End-to-end workflows    | Selenium, PyQt testing | 70%+          |
| **Performance Testing** | Load and stress testing | pytest-benchmark       | Key scenarios |

### **Test Categories**

1. **Functional Tests**: All calculation modules and features
2. **UI Tests**: User interface interactions and workflows
3. **Data Tests**: Database operations and file I/O
4. **Performance Tests**: Response times and memory usage
5. **Compatibility Tests**: Cross-platform functionality

---

## 📦 **Deployment Strategy**

### **Distribution Methods**

| Platform    | Format                  | Size   | Dependencies |
| ----------- | ----------------------- | ------ | ------------ |
| **Windows** | .exe (PyInstaller)      | ~150MB | None         |
| **macOS**   | .app (PyInstaller)      | ~150MB | None         |
| **Linux**   | .AppImage (PyInstaller) | ~150MB | None         |
| **Source**  | Python package          | ~50MB  | Python 3.9+  |

### **Installation Options**

1. **Standard Installer**: MSI/DEB/RPM packages with system integration
2. **Portable Version**: No installation required, runs from any directory
3. **Enterprise Deployment**: Silent installation with group policy support
4. **Development Setup**: Source code installation with virtual environment

---

## 📈 **Development Phases**

### **Phase 1: Requirements Analysis** ✅ **COMPLETE**

- [x] Software Requirements Specification (SRS)
- [x] Functional requirements definition
- [x] Non-functional requirements definition
- [x] User stories and use cases
- [x] System architecture design

### **Phase 2: System Design** ✅ **COMPLETE**

- [x] Detailed system design
- [x] Database schema design
- [x] API specifications
- [x] UI/UX mockups
- [x] Module interface definitions
- [x] Class diagrams and relationships
- [x] Process flow diagrams
- [x] Performance specifications

### **Phase 3: Implementation** 🔄 **NEXT**

- [ ] Core calculator engine
- [ ] GUI implementation
- [ ] Engineering modules
- [ ] Visualization system
- [ ] Data persistence
- [ ] Module plugin system
- [ ] Export/import functionality
- [ ] Settings management

### **Phase 4: Testing & Deployment** ⏳ **PENDING**

- [ ] Unit testing
- [ ] Integration testing
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Distribution packaging
- [ ] Documentation completion

---

## ✅ **Design Validation**

### **Architecture Validation**

- ✅ **Separation of Concerns**: Clear layer boundaries
- ✅ **Loose Coupling**: Well-defined interfaces
- ✅ **High Cohesion**: Related functionality grouped
- ✅ **Scalability**: Modular design supports growth
- ✅ **Maintainability**: Clean code structure

### **Performance Validation**

- ✅ **Response Time**: All targets achievable
- ✅ **Memory Usage**: Efficient resource management
- ✅ **Scalability**: Handles large datasets
- ✅ **Concurrency**: Multi-threaded processing

### **Usability Validation**

- ✅ **Intuitive Interface**: Standard engineering software conventions
- ✅ **Accessibility**: Keyboard navigation and screen reader support
- ✅ **Responsive Design**: Adapts to different screen sizes
- ✅ **Error Handling**: Clear, actionable error messages

---

## 🎯 **Success Criteria**

### **Functional Success**

- [ ] All calculation modules produce accurate results
- [ ] .ecp file format works correctly
- [ ] Visualization generates proper charts
- [ ] Export functions work for all formats
- [ ] Module system allows plugin installation
- [ ] Error handling provides clear messages
- [ ] Settings system controls all preferences

### **Non-Functional Success**

- [ ] Performance meets all specified targets
- [ ] Application runs on all target platforms
- [ ] Auto-save functionality works reliably
- [ ] Interface is intuitive for new users
- [ ] Modular architecture supports extensibility

---

**Document Status**: ✅ **COMPLETE**  
**Next Phase**: Implementation  
**Approval**: Ready for Phase 3 Development

---

## 📚 **Documentation Deliverables**

1. **System Design Document** (`docs/System_Design.md`) - Complete system architecture
2. **Class Diagrams** (`docs/Class_Diagrams.md`) - Detailed UML class diagrams
3. **GUI Mockups** (`docs/GUI_Mockups.md`) - User interface designs and specifications
4. **Flow Diagrams** (`docs/Flow_Diagrams.md`) - Process and data flow diagrams
5. **System Design Summary** (`docs/System_Design_Summary.md`) - This comprehensive overview

**Total Documentation**: 5 comprehensive documents covering all aspects of system design
