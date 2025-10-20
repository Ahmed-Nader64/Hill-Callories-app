# Class Diagrams
## HeroCal - Engineering Calculator Application

---

## 1. Main Application Classes

### 1.1 Core Application Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MainWindow                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ - ui_components: Dict[str, QWidget]                                        │
│ - current_project: Optional[Project]                                       │
│ - calculation_engine: CalculationEngine                                    │
│ - module_manager: ModuleManager                                            │
│ - settings_manager: SettingsManager                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + setup_ui()                                                               │
│ + setup_connections()                                                      │
│ + open_project(file_path: str) -> bool                                     │
│ + save_project(file_path: str = None) -> bool                              │
│ + show_results(results: CalculationResults)                                │
│ + show_module_dialog(module_name: str)                                     │
│ + update_status_bar(message: str)                                          │
│ + closeEvent(event: QCloseEvent)                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CalculationEngine                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ - modules: Dict[str, BaseModule]                                           │
│ - validation_service: ValidationService                                    │
│ - cache_manager: CacheManager                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + register_module(module: BaseModule) -> bool                              │
│ + unregister_module(module_name: str) -> bool                              │
│ + calculate(module_name: str, inputs: Dict) -> CalculationResult           │
│ + validate_inputs(module_name: str, inputs: Dict) -> ValidationResult      │
│ + get_available_modules() -> List[str]                                     │
│ + get_module_info(module_name: str) -> Optional[ModuleInfo]                │
│ + clear_cache()                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ModuleManager                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ - builtin_modules: Dict[str, Type[BaseModule]]                             │
│ - plugin_modules: Dict[str, BaseModule]                                    │
│ - module_registry: ModuleRegistry                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + load_builtin_modules()                                                   │
│ + scan_plugin_modules()                                                    │
│ + load_module(module_path: str) -> bool                                    │
│ + unload_module(module_name: str) -> bool                                  │
│ + get_module_info(module_name: str) -> ModuleInfo                          │
│ + register_module(module_class: Type[BaseModule])                          │
│ + get_enabled_modules() -> List[str]                                       │
│ + enable_module(module_name: str) -> bool                                  │
│ + disable_module(module_name: str) -> bool                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Management Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ProjectManager                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ - database: ProjectDatabase                                                │
│ - file_manager: FileSystemManager                                          │
│ - export_service: ExportService                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + create_project(name: str, description: str) -> Project                   │
│ + load_project(file_path: str) -> Project                                  │
│ + save_project(project: Project, file_path: str = None) -> bool            │
│ + export_project(project: Project, format: str, file_path: str) -> bool    │
│ + get_recent_projects(limit: int = 10) -> List[Project]                    │
│ + delete_project(project_id: int) -> bool                                  │
│ + duplicate_project(project: Project, new_name: str) -> Project            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Project                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ - id: Optional[int]                                                        │
│ - name: str                                                                │
│ - description: str                                                         │
│ - created_date: datetime                                                   │
│ - modified_date: datetime                                                  │
│ - settings: Dict[str, Any]                                                 │
│ - calculations: List[Calculation]                                          │
│ - metadata: Dict[str, Any]                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__(name: str, description: str = "")                               │
│ + add_calculation(calculation: Calculation)                                │
│ + get_calculation_history() -> List[Calculation]                           │
│ + update_metadata(key: str, value: Any)                                    │
│ + get_setting(key: str, default: Any = None) -> Any                        │
│ + set_setting(key: str, value: Any)                                        │
│ + serialize() -> Dict[str, Any]                                            │
│ + deserialize(data: Dict[str, Any])                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Calculation                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ - id: Optional[int]                                                        │
│ - module_name: str                                                         │
│ - calculation_type: str                                                    │
│ - input_data: Dict[str, Any]                                               │
│ - results: Dict[str, Any]                                                  │
│ - created_date: datetime                                                   │
│ - execution_time_ms: int                                                   │
│ - charts: List[Chart]                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__(module_name: str, inputs: Dict, results: Dict)                  │
│ + add_chart(chart: Chart)                                                  │
│ + get_charts() -> List[Chart]                                              │
│ + serialize() -> Dict[str, Any]                                            │
│ + deserialize(data: Dict[str, Any])                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Module System Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            BaseModule                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ - module_info: ModuleInfo                                                  │
│ - is_enabled: bool                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ + get_info() -> ModuleInfo                                                 │
│ + validate_inputs(inputs: Dict[str, Any]) -> Dict[str, str]                │
│ + calculate(inputs: Dict[str, Any]) -> Dict[str, Any]                      │
│ + create_chart(inputs: Dict, results: Dict, chart_type: str) -> Dict       │
│ + get_input_fields() -> List[InputField]                                   │
│ + get_output_fields() -> List[OutputField]                                 │
│ + enable()                                                                │
│ + disable()                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│   StructuralModule      │ │   ElectricalModule      │ │   ThermalModule         │
├─────────────────────────┤ ├─────────────────────────┤ ├─────────────────────────┤
│ - beam_analysis:        │ │ - dc_circuit_analysis:  │ │ - heat_transfer:        │
│   BeamAnalysis          │ │   DCCircuitAnalysis     │ │   HeatTransferAnalysis  │
│ - stress_analysis:      │ │ - ac_circuit_analysis:  │ │ - ideal_gas_law:        │
│   StressAnalysis        │ │   ACCircuitAnalysis     │ │   IdealGasLawAnalysis   │
│ - column_analysis:      │ │ - power_analysis:       │ │ - efficiency_analysis:  │
│   ColumnAnalysis        │ │   PowerAnalysis         │ │   EfficiencyAnalysis    │
├─────────────────────────┤ ├─────────────────────────┤ ├─────────────────────────┤
│ + get_info() ->         │ │ + get_info() ->         │ │ + get_info() ->         │
│   ModuleInfo            │ │   ModuleInfo            │ │   ModuleInfo            │
│ + validate_inputs() ->  │ │ + validate_inputs() ->  │ │ + validate_inputs() ->  │
│   Dict[str, str]        │ │   Dict[str, str]        │ │   Dict[str, str]        │
│ + calculate() ->        │ │ + calculate() ->        │ │ + calculate() ->        │
│   Dict[str, Any]        │ │   Dict[str, Any]        │ │   Dict[str, Any]        │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

### 1.4 Specific Engineering Module Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BeamAnalysis                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ - support_types: List[str]                                                 │
│ - material_properties: Dict[str, float]                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + get_info() -> ModuleInfo                                                 │
│ + validate_inputs(inputs: Dict) -> Dict[str, str]                          │
│ + calculate(inputs: Dict) -> Dict[str, Any]                                │
│ + calculate_deflection(length: float, load: float, inertia: float,        │
│   elasticity: float, support_type: str) -> float                           │
│ + calculate_stress(moment: float, inertia: float, distance: float) -> float│
│ + calculate_reactions(load: float, position: float, length: float) ->      │
│   Tuple[float, float]                                                      │
│ + create_deflection_chart(inputs: Dict, results: Dict) -> Dict             │
│ + create_moment_chart(inputs: Dict, results: Dict) -> Dict                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        DCCircuitAnalysis                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ - circuit_types: List[str]                                                 │
│ - component_types: Dict[str, str]                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + get_info() -> ModuleInfo                                                 │
│ + validate_inputs(inputs: Dict) -> Dict[str, str]                          │
│ + calculate(inputs: Dict) -> Dict[str, Any]                                │
│ + calculate_ohm_law(voltage: float, current: float, resistance: float) ->  │
│   Dict[str, float]                                                         │
│ + calculate_power(voltage: float, current: float, resistance: float) ->    │
│   Dict[str, float]                                                         │
│ + calculate_series_resistance(resistances: List[float]) -> float           │
│ + calculate_parallel_resistance(resistances: List[float]) -> float         │
│ + create_circuit_diagram(inputs: Dict, results: Dict) -> Dict              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.5 Data Layer Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ProjectDatabase                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ - db_path: str                                                             │
│ - connection: sqlite3.Connection                                           │
│ - cursor: sqlite3.Cursor                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__(db_path: str)                                                   │
│ + init_database()                                                          │
│ + create_project(name: str, description: str) -> int                       │
│ + save_calculation(project_id: int, module_name: str, inputs: Dict,        │
│   results: Dict) -> int                                                    │
│ + load_project(project_id: int) -> Project                                 │
│ + get_calculation_history(project_id: int) -> List[Calculation]            │
│ + update_project_metadata(project_id: int, metadata: Dict)                 │
│ + delete_project(project_id: int) -> bool                                  │
│ + search_projects(query: str) -> List[Project]                             │
│ + get_project_statistics() -> Dict[str, int]                               │
│ + close()                                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FileSystemManager                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ - project_directory: str                                                   │
│ - backup_directory: str                                                    │
│ - temp_directory: str                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__(project_dir: str)                                               │
│ + save_project_file(project: Project, file_path: str) -> bool              │
│ + load_project_file(file_path: str) -> Project                             │
│ + create_backup(project: Project) -> str                                   │
│ + restore_backup(backup_path: str) -> Project                              │
│ + export_to_pdf(project: Project, file_path: str) -> bool                  │
│ + export_to_excel(project: Project, file_path: str) -> bool                │
│ + export_to_csv(project: Project, file_path: str) -> bool                  │
│ + validate_ecp_file(file_path: str) -> bool                                │
│ + cleanup_temp_files()                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.6 Visualization Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      VisualizationManager                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ - chart_templates: Dict[str, ChartTemplate]                                │
│ - active_charts: Dict[str, Chart]                                          │
│ - matplotlib_backend: str                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + create_chart(chart_type: str, data: Dict, options: Dict = None) -> Chart │
│ + update_chart(chart_id: str, new_data: Dict)                             │
│ + export_chart(chart: Chart, format: str, file_path: str)                 │
│ + get_chart_templates() -> List[str]                                       │
│ + register_chart_template(template: ChartTemplate)                         │
│ + clear_charts()                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Chart                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ - chart_id: str                                                            │
│ - chart_type: str                                                          │
│ - title: str                                                               │
│ - x_label: str                                                             │
│ - y_label: str                                                             │
│ - data: Dict[str, Any]                                                     │
│ - options: Dict[str, Any]                                                  │
│ - created_date: datetime                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__(chart_type: str, data: Dict, options: Dict = None)              │
│ + update_data(new_data: Dict)                                              │
│ + export(format: str, file_path: str) -> bool                              │
│ + get_image_data(format: str = 'png') -> bytes                             │
│ + serialize() -> Dict[str, Any]                                            │
│ + deserialize(data: Dict[str, Any])                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.7 Settings and Configuration Classes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SettingsManager                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ - settings_file: str                                                       │
│ - settings: Dict[str, Any]                                                 │
│ - default_settings: Dict[str, Any]                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + load_settings()                                                          │
│ + save_settings()                                                          │
│ + get_setting(key: str, default: Any = None) -> Any                        │
│ + set_setting(key: str, value: Any)                                        │
│ + reset_to_defaults()                                                      │
│ + get_all_settings() -> Dict[str, Any]                                     │
│ + validate_settings(settings: Dict[str, Any]) -> bool                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ValidationService                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ - validation_rules: Dict[str, ValidationRule]                              │
│ - unit_converter: UnitConverter                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ + __init__()                                                               │
│ + validate_numeric_input(value: str, min_val: float = None,                │
│   max_val: float = None) -> ValidationResult                               │
│ + validate_unit_conversion(value: float, from_unit: str, to_unit: str) ->  │
│   ValidationResult                                                         │
│ + validate_engineering_input(module_name: str, inputs: Dict) ->            │
│   ValidationResult                                                         │
│ + register_validation_rule(rule_name: str, rule: ValidationRule)           │
│ + get_validation_errors(inputs: Dict) -> List[str]                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Transfer Objects (DTOs)

### 2.1 Core DTOs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ModuleInfo                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ + name: str                                                                │
│ + version: str                                                             │
│ + description: str                                                         │
│ + category: str                                                            │
│ + author: str                                                              │
│ + input_fields: List[InputField]                                           │
│ + output_fields: List[OutputField]                                         │
│ + chart_types: List[str]                                                   │
│ + dependencies: List[str]                                                  │
│ + license: str                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          InputField                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ + name: str                                                                │
│ + label: str                                                               │
│ + field_type: str                                                          │
│ + default_value: Any                                                       │
│ + min_value: Optional[float]                                               │
│ + max_value: Optional[float]                                               │
│ + unit: Optional[str]                                                      │
│ + required: bool                                                           │
│ + description: str                                                         │
│ + validation_rules: List[str]                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          OutputField                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ + name: str                                                                │
│ + label: str                                                               │
│ + unit: str                                                                │
│ + precision: int                                                           │
│ + description: str                                                         │
│ + format_string: str                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       CalculationResult                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ + success: bool                                                            │
│ + results: Dict[str, Any]                                                  │
│ + errors: List[str]                                                        │
│ + warnings: List[str]                                                      │
│ + execution_time_ms: int                                                   │
│ + module_name: str                                                         │
│ + timestamp: datetime                                                      │
│ + charts: List[Chart]                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       ValidationResult                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ + is_valid: bool                                                           │
│ + errors: Dict[str, str]                                                   │
│ + warnings: Dict[str, str]                                                 │
│ + suggestions: Dict[str, str]                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Class Relationships

### 3.1 Inheritance Hierarchy

```
BaseModule (Abstract)
    ├── StructuralModule
    │   ├── BeamAnalysis
    │   ├── StressAnalysis
    │   └── ColumnAnalysis
    ├── ElectricalModule
    │   ├── DCCircuitAnalysis
    │   ├── ACCircuitAnalysis
    │   └── PowerAnalysis
    └── ThermalModule
        ├── HeatTransferAnalysis
        ├── IdealGasLawAnalysis
        └── EfficiencyAnalysis

QMainWindow
    └── MainWindow

QDialog
    ├── ModuleDialog
    ├── SettingsDialog
    └── ExportDialog

QWidget
    ├── VisualizationWidget
    ├── InputPanel
    └── ResultsPanel
```

### 3.2 Composition Relationships

```
MainWindow
    ├── CalculationEngine
    ├── ModuleManager
    ├── ProjectManager
    ├── SettingsManager
    └── VisualizationManager

CalculationEngine
    ├── ValidationService
    └── CacheManager

ProjectManager
    ├── ProjectDatabase
    └── FileSystemManager

Project
    └── List<Calculation>

Calculation
    └── List<Chart>
```

### 3.3 Dependency Relationships

```
MainWindow → CalculationEngine → BaseModule
MainWindow → ProjectManager → Project
MainWindow → VisualizationManager → Chart
CalculationEngine → ValidationService
ProjectManager → ProjectDatabase
ProjectManager → FileSystemManager
```

---

**Document Status**: ✅ **COMPLETE**  
**Next Phase**: Implementation  
**Approval**: Ready for Phase 3 Development
