# Software Requirements Specification (SRS)

## HeroCal - Engineering Calculator Application

**Version:** 1.0  
**Date:** December 2024  
**Author:** HeroCal Development Team

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for HeroCal, a comprehensive engineering calculator application that combines traditional calculator functionality with advanced engineering analysis tools, data visualization, and project management capabilities.

### 1.2 Scope

HeroCal is a desktop application designed for engineers, students, and technical professionals who need:

- Advanced mathematical computations
- Engineering-specific calculations
- Data visualization and plotting
- Project saving and management
- Cross-platform compatibility (Windows, Linux, macOS)

### 1.3 Definitions and Acronyms

- **SRS**: Software Requirements Specification
- **GUI**: Graphical User Interface
- **API**: Application Programming Interface
- **SQLite**: Lightweight database engine
- **PyQt6**: Python GUI framework

---

## 2. Overall Description

### 2.1 Product Perspective

HeroCal is a standalone desktop application that operates independently of other software systems. It provides a comprehensive engineering calculation environment with the following key components:

- **Core Calculator Engine**: Mathematical computation backend
- **GUI Interface**: User-friendly graphical interface
- **Data Visualization**: Plotting and charting capabilities
- **Data Persistence**: Local database for saving projects and history
- **Memory Management**: Calculation memory and history features

### 2.2 Product Functions

#### 2.2.1 Core Calculator Functions

- Basic arithmetic operations (+, -, ×, ÷)
- Advanced mathematical functions (sin, cos, tan, log, ln, sqrt, etc.)
- Engineering constants (π, e, gravitational acceleration, etc.)
- Unit conversions (length, area, volume, pressure, temperature, etc.)
- Memory functions (M+, M-, MR, MC, MS)

#### 2.2.2 Engineering Analysis Functions

- **Structural Analysis**

  - Beam deflection calculations
  - Stress and strain analysis
  - Moment and shear force calculations
  - Column buckling analysis

- **Mechanical Analysis**

  - Gear ratio calculations
  - Belt and pulley systems
  - Spring calculations
  - Fluid mechanics (Bernoulli's equation, Reynolds number)

- **Electrical Analysis**

  - Ohm's law calculations
  - Power calculations (P = VI, P = I²R)
  - Series and parallel circuit analysis
  - AC circuit calculations

- **Thermodynamics**
  - Heat transfer calculations
  - Ideal gas law
  - Efficiency calculations
  - Temperature conversions

#### 2.2.3 Data Visualization

- Function plotting (2D graphs)
- Data point plotting
- Engineering charts (stress-strain, load-deflection)
- Export capabilities (PNG, PDF, SVG)

#### 2.2.4 Project Management

- Save calculation projects
- Load previous projects
- Calculation history
- Export results to various formats

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Calculation Modules Requirements

**FR-CM-001**: **Modular Calculation System**

- The application shall support pluggable calculation modules for different engineering disciplines
- Users shall be able to add/remove analysis modules through a module manager interface
- Each module shall be self-contained with its own input validation and output formatting
- Modules shall include: Structural Analysis, Mechanical Analysis, Electrical Analysis, Thermodynamics, Fluid Mechanics

**FR-CM-002**: **Beam Deflection Module**

- **Inputs**: Beam length (L), applied load (P), moment of inertia (I), modulus of elasticity (E), support conditions
- **Outputs**: Maximum deflection, deflection at any point, maximum stress, reaction forces
- **Formula Support**: Simply supported, cantilever, fixed-fixed beam configurations

**FR-CM-003**: **Stress Analysis Module**

- **Inputs**: Applied force (F), cross-sectional area (A), material properties, loading conditions
- **Outputs**: Normal stress, shear stress, von Mises stress, safety factor, factor of safety
- **Support**: Axial, bending, torsional, and combined loading scenarios

**FR-CM-004**: **Electrical Circuit Module**

- **Inputs**: Voltage (V), current (I), resistance (R), power (P), frequency (f)
- **Outputs**: Missing electrical parameters, power dissipation, impedance, phase angle
- **Support**: DC circuits, AC circuits, series/parallel combinations

#### 3.1.2 Graphical Visualization Requirements

**FR-GV-001**: **Chart and Diagram Generation**

- The application shall generate engineering charts using Matplotlib or Plotly
- Support for 2D plotting with customizable axes, labels, and grid
- Real-time chart updates as input parameters change
- Interactive zoom, pan, and data point inspection capabilities

**FR-GV-002**: **Engineering-Specific Visualizations**

- Stress-strain curves with material property overlays
- Load-deflection diagrams for structural analysis
- Frequency response plots for dynamic analysis
- Temperature distribution plots for thermal analysis

**FR-GV-003**: **Export Visualization**

- Export charts to PNG, PDF, SVG formats
- High-resolution output suitable for technical reports
- Batch export of multiple charts

#### 3.1.3 File I/O Requirements

**FR-FIO-001**: **Project File Format (.ecp)**

- The application shall use a custom .ecp (Engineering Calculator Project) file format
- Files shall contain: calculation inputs, results, charts, project metadata, module configurations
- Files shall be human-readable JSON format for debugging and manual editing
- Support for project versioning and backward compatibility

**FR-FIO-002**: **Project Management**

- Save projects with user-defined names and descriptions
- Load projects with full restoration of calculation state
- Project templates for common engineering scenarios
- Recent projects list with quick access

**FR-FIO-003**: **Auto-Save Functionality**

- Automatic project saving every 5 minutes during active use
- Manual save triggers on significant calculation changes
- Recovery of unsaved work on application restart
- Configurable auto-save intervals

#### 3.1.4 Export Results Requirements

**FR-ER-001**: **Report Generation**

- Export comprehensive calculation reports as PDF with professional formatting
- Include input parameters, calculation steps, results, and charts
- Customizable report templates for different engineering disciplines
- Batch export of multiple calculations

**FR-ER-002**: **Data Export Formats**

- Excel (.xlsx) export with multiple worksheets for different calculation modules
- CSV export for data analysis in external tools
- JSON export for programmatic access to calculation data
- LaTeX export for academic and technical documentation

#### 3.1.5 Modular System Requirements

**FR-MS-001**: **Plugin Architecture**

- Support for third-party calculation modules through standardized API
- Module discovery and loading system
- Module dependency management
- Hot-swapping of modules without application restart

**FR-MS-002**: **Module Management Interface**

- Visual module manager showing installed/available modules
- Module configuration and parameter setup
- Module documentation and help system
- Module performance monitoring and optimization

#### 3.1.6 Error Handling Requirements

**FR-EH-001**: **User-Friendly Error Messages**

- Clear, actionable error messages for invalid inputs
- Context-sensitive help for error resolution
- Input validation with real-time feedback
- Error logging for debugging and improvement

**FR-EH-002**: **Robust Error Recovery**

- Graceful handling of calculation errors without application crash
- Automatic input validation and correction suggestions
- Undo/redo functionality for error recovery
- Error reporting system for continuous improvement

#### 3.1.7 Settings System Requirements

**FR-SS-001**: **Unit System Management**

- Support for SI (International System) and Imperial units
- Automatic unit conversion between systems
- Custom unit definitions for specialized applications
- Unit consistency checking across calculations

**FR-SS-002**: **Theme and Appearance**

- Dark and light theme options with smooth transitions
- Customizable color schemes for different engineering disciplines
- Font size and style customization for accessibility
- High contrast mode for visual accessibility

**FR-SS-003**: **Precision Control**

- Configurable decimal precision (1-15 digits)
- Scientific notation display options
- Significant figure handling
- Rounding mode selection (round, floor, ceiling, truncate)

#### 3.1.8 Auto-Update and Versioning Requirements

**FR-AU-001**: **Update Notification System**

- Check for updates on application startup (optional)
- Display update notifications with version information
- Download and install updates with user confirmation
- Rollback capability for problematic updates

**FR-AU-002**: **Version Management**

- Semantic versioning (Major.Minor.Patch)
- Changelog display for each version
- Module-specific version tracking
- Compatibility checking for project files

#### 3.1.9 Authentication Requirements (Future)

**FR-AUTH-001**: **Optional Login System**

- User account creation and management
- Secure authentication with password encryption
- Pro feature access control
- Cloud synchronization (optional, user-controlled)

#### 3.1.10 User Interface Requirements

**FR-UI-001**: **Intuitive GUI Design**

- Clean, professional interface following engineering software conventions
- Organized function groups with collapsible sections
- Keyboard shortcuts for all major functions
- Context-sensitive help and tooltips

**FR-UI-002**: **Responsive Interface**

- Real-time input validation and feedback
- Progress indicators for long calculations
- Non-blocking UI during computation
- Multi-threaded calculation processing

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance Requirements

**NFR-PERF-001**: **Computation Performance**

- All engineering calculations shall complete within 1 second per calculation
- Complex multi-step calculations shall complete within 5 seconds maximum
- Real-time chart updates shall refresh within 500 milliseconds
- Application startup time shall be under 3 seconds

**NFR-PERF-002**: **User Interface Responsiveness**

- User input response time shall be under 100 milliseconds
- GUI shall remain responsive during background calculations
- Chart rendering shall not block user interface interactions
- Memory usage shall not exceed 500MB during normal operation

**NFR-PERF-003**: **Data Processing**

- Support for calculations with up to 15 significant digits precision
- Handle datasets with up to 10,000 data points for visualization
- Project file loading/saving shall complete within 2 seconds
- Batch export operations shall process 100+ calculations within 30 seconds

#### 3.2.2 Usability Requirements

**NFR-USE-001**: **Intuitive Interface**

- New users shall be able to perform basic calculations within 5 minutes of first use
- Interface shall follow standard engineering software conventions
- All functions shall be discoverable through logical menu organization
- Context-sensitive help shall be available for all features

**NFR-USE-002**: **Accessibility**

- Support for keyboard navigation of all interface elements
- High contrast mode for users with visual impairments
- Configurable font sizes and styles
- Screen reader compatibility for accessibility tools

**NFR-USE-003**: **Learning Curve**

- Comprehensive help documentation with examples
- Interactive tutorials for each calculation module
- Tooltips and inline help for all input fields
- Video tutorials for complex engineering calculations

#### 3.2.3 Reliability Requirements

**NFR-REL-001**: **Data Persistence**

- Automatic data saving every 5 minutes during active use
- No data loss during unexpected application shutdown
- Project recovery system for corrupted files
- Backup creation for critical calculation data

**NFR-REL-002**: **Error Handling**

- Application shall gracefully handle all error conditions without crashing
- Invalid input validation with clear error messages
- Calculation error recovery with suggested corrections
- Comprehensive error logging for debugging and improvement

**NFR-REL-003**: **System Stability**

- Application shall run continuously for 8+ hours without memory leaks
- Module loading/unloading shall not affect system stability
- Concurrent calculation processing without conflicts
- Graceful degradation when system resources are limited

#### 3.2.4 Portability Requirements

**NFR-PORT-001**: **Cross-Platform Support**

- Windows 10/11 (x64 architecture)
- macOS 10.15+ (Intel and Apple Silicon)
- Linux Ubuntu 18.04+ and compatible distributions
- Consistent functionality and performance across all platforms

**NFR-PORT-002**: **Installation and Distribution**

- Standalone executable distribution (no Python installation required)
- Portable version that runs from USB drives
- Silent installation options for enterprise deployment
- Automatic dependency resolution and installation

#### 3.2.5 Security Requirements

**NFR-SEC-001**: **Data Security**

- All user data shall be stored locally on the user's machine
- No transmission of calculation data over the network
- Project files shall be encrypted with user-defined passwords (optional)
- Secure deletion of temporary files and calculation history

**NFR-SEC-002**: **Privacy Protection**

- No telemetry or usage tracking without explicit user consent
- Local-only operation with no cloud dependencies
- User control over all data storage and sharing
- Compliance with data protection regulations (GDPR, CCPA)

#### 3.2.6 Maintainability Requirements

**NFR-MAIN-001**: **Modular Architecture**

- Plugin-based system allowing easy addition of new calculation modules
- Standardized API for third-party module development
- Clear separation of concerns between GUI, business logic, and data layers
- Comprehensive unit test coverage for all core functionality

**NFR-MAIN-002**: **Code Quality**

- Well-documented source code with inline comments
- Consistent coding standards and style guidelines
- Automated testing and continuous integration
- Regular code reviews and refactoring cycles

#### 3.2.7 Scalability Requirements

**NFR-SCAL-001**: **Module Scalability**

- Support for unlimited number of calculation modules
- Dynamic loading of modules based on user needs
- Module dependency management and conflict resolution
- Performance optimization for large module collections

**NFR-SCAL-002**: **Data Scalability**

- Efficient handling of large calculation datasets
- Optimized database queries for project management
- Memory-efficient chart rendering for large datasets
- Batch processing capabilities for multiple calculations

---

## 3.3 Requirements Summary

### 🎯 Functional Requirements Summary

| Feature                         | Description                                                                     | Priority |
| ------------------------------- | ------------------------------------------------------------------------------- | -------- |
| **1. Calculation Modules**      | Perform formulas (e.g., beam deflection, stress, etc.) with user-defined inputs | High     |
| **2. Graphical Visualization**  | Show charts/diagrams using Matplotlib or Plotly                                 | High     |
| **3. File I/O**                 | Save and open projects (.ecp files)                                             | High     |
| **4. Export Results**           | Export reports as .pdf, .xlsx, .csv                                             | Medium   |
| **5. Modular System**           | Allow adding/removing analysis modules easily                                   | High     |
| **6. Error Handling**           | Display user-friendly error messages (e.g., invalid input)                      | High     |
| **7. Settings System**          | Units (SI/Imperial), themes (dark/light), precision control                     | Medium   |
| **8. Auto-update & Versioning** | Notify user when an update is available (optional)                              | Low      |
| **9. Authentication**           | Optional — login system for pro features (future)                               | Low      |

### 🧍‍♂️ Non-Functional Requirements Summary

| Type                | Specification                                |
| ------------------- | -------------------------------------------- |
| **Performance**     | Computation time < 1 sec per calculation     |
| **Usability**       | GUI must be intuitive and responsive         |
| **Reliability**     | Save data automatically every 5 minutes      |
| **Portability**     | Windows, Linux, macOS                        |
| **Maintainability** | Modular architecture (new modules = plug-in) |

---

## 4. User Stories

### 4.1 Basic Calculator Stories

**US-001**: As a user, I want to perform basic arithmetic operations so that I can quickly calculate simple math problems.

**US-002**: As a user, I want to use scientific functions (sin, cos, log, etc.) so that I can perform advanced mathematical calculations.

**US-003**: As a user, I want to store values in memory so that I can reuse them in subsequent calculations.

### 4.2 Engineering Analysis Stories

**US-004**: As a structural engineer, I want to calculate beam deflection so that I can verify that my design meets deflection limits.

**US-005**: As a mechanical engineer, I want to calculate stress in a component so that I can ensure it won't fail under load.

**US-006**: As an electrical engineer, I want to analyze circuit parameters so that I can design safe and efficient electrical systems.

**US-007**: As an engineer, I want to convert between different units so that I can work with international standards and specifications.

### 4.3 Data Management Stories

**US-008**: As a user, I want to save my calculation projects so that I can return to them later.

**US-009**: As a user, I want to view my calculation history so that I can review previous work.

**US-010**: As a user, I want to export my results so that I can include them in reports and documentation.

### 4.4 Visualization Stories

**US-011**: As a user, I want to plot mathematical functions so that I can visualize relationships between variables.

**US-012**: As an engineer, I want to create engineering charts so that I can present my analysis results graphically.

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Business Logic │    │  Data Layer     │
│   (PyQt6)       │◄──►│     Layer       │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │
│ - Main Window   │    │ - Calculator    │    │ - Projects DB   │
│ - Dialogs       │    │ - Engineering   │    │ - History DB    │
│ - Widgets       │    │ - Visualization │    │ - Settings      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 5.2 Component Overview

- **GUI Layer**: PyQt6-based user interface
- **Business Logic**: Core calculation engine and engineering functions
- **Data Layer**: SQLite database for persistence
- **Visualization**: Matplotlib integration for plotting

---

## 6. Acceptance Criteria

### 6.1 Functional Acceptance Criteria

- [ ] All basic calculator functions work correctly
- [ ] All engineering analysis functions produce accurate results
- [ ] Memory functions store and recall values properly
- [ ] Data visualization creates accurate plots and charts
- [ ] Project saving and loading works without data loss
- [ ] Unit conversions are accurate to at least 6 decimal places

### 6.2 Non-Functional Acceptance Criteria

- [ ] Application starts within 3 seconds
- [ ] User interface responds within 100ms to input
- [ ] Application runs without crashes for 8+ hours
- [ ] All features work consistently across Windows, macOS, and Linux
- [ ] Help documentation is complete and accessible

---

## 7. Constraints and Assumptions

### 7.1 Constraints

- Application must run on desktop platforms only
- All data must be stored locally (no cloud features)
- Must use Python as the primary programming language
- Must be distributable as a standalone executable

### 7.2 Assumptions

- Users have basic familiarity with calculator interfaces
- Users understand basic engineering concepts
- System has sufficient memory for mathematical computations
- Users prefer local data storage over cloud-based solutions

---

## 8. Future Enhancements

### 8.1 Potential Future Features

- 3D visualization capabilities
- Advanced finite element analysis
- Integration with CAD software
- Cloud synchronization (optional)
- Mobile companion app
- Plugin system for custom functions

---

**Document Status**: Draft  
**Next Review Date**: TBD  
**Approval Required**: Development Team Lead
