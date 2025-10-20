# HeroCal - Engineering Calculator

A comprehensive engineering calculator application with modular analysis capabilities, built with Python and PyQt6.

## Features

### 🏗️ **Modular Architecture**

- **Structural Analysis**: Beam deflection, stress analysis, moment calculations
- **Electrical Analysis**: DC/AC circuit analysis, power calculations
- **Thermal Analysis**: Heat transfer, thermodynamics, efficiency calculations
- **Extensible Plugin System**: Add custom calculation modules

### 🎨 **Modern GUI**

- **Professional Interface**: Clean, intuitive design following engineering software conventions
- **Dark/Light Themes**: Multiple theme options with high contrast support
- **Responsive Layout**: Adapts to different screen sizes and window configurations
- **Real-time Validation**: Input validation with helpful error messages

### 📊 **Advanced Visualization**

- **Interactive Charts**: Matplotlib and Plotly integration for dynamic visualizations
- **Engineering Diagrams**: Specialized charts for structural, electrical, and thermal analysis
- **Export Capabilities**: Save charts in PNG, PDF, SVG formats
- **Real-time Updates**: Charts update automatically with calculation changes

### 💾 **Data Management**

- **Project Files**: Save and load calculation projects (.ecp format)
- **Auto-save**: Automatic saving every 5 minutes to prevent data loss
- **Calculation History**: Track and recall previous calculations
- **Export Options**: PDF reports, Excel spreadsheets, CSV data

### ⚡ **Performance**

- **Fast Calculations**: < 1 second execution time for most calculations
- **Multi-threading**: Non-blocking UI during complex computations
- **Memory Efficient**: Optimized for large datasets and long sessions
- **Caching**: Intelligent result caching for improved performance

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/herocal.git
   cd herocal
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Test installation**

   ```bash
   python test_installation.py
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Development Setup

1. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**

   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-qt
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

## Usage

### Getting Started

1. **Launch HeroCal**

   ```bash
   python main.py
   ```

2. **Select a Module**

   - Choose from Structural, Electrical, or Thermal analysis modules
   - Click on a module in the left panel to select it

3. **Enter Parameters**

   - Fill in the required input parameters in the center panel
   - The system will validate inputs in real-time

4. **Calculate Results**

   - Click "Calculate" to perform the analysis
   - View results in the results panel
   - Examine charts in the visualization panel

5. **Save Your Work**
   - Use File → Save Project to save your calculations
   - Export results to PDF or Excel formats

### Example: Beam Analysis

1. Select "Structural" → "Beam Analysis"
2. Enter parameters:
   - Beam Length: 5.0 m
   - Applied Load: 1000 N
   - Moment of Inertia: 0.001 m⁴
   - Modulus of Elasticity: 200 GPa
   - Support Type: Simply Supported
3. Click "Calculate"
4. View results: deflection, stress, reactions, safety factor
5. Examine deflection and moment diagrams

## Architecture

### 3-Tier Layered Design

```
┌─────────────────────────────────────────────────────────────┐
│                PRESENTATION LAYER (GUI)                     │
│  PyQt6 + QML + CSS Styling                                 │
│  • MainWindow, Module Dialogs, Visualization Widgets       │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 LOGIC LAYER (SERVICES)                      │
│  Python Classes & Services                                 │
│  • CalculationEngine, ModuleManager, VisualizationManager  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 DATA LAYER (STORAGE)                        │
│  SQLite / JSON / ConfigParser                              │
│  • ProjectDatabase, SettingsManager, FileSystemManager     │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

- **Calculation Engine**: Core computation and module management
- **Data Manager**: Project persistence and file I/O
- **Settings Manager**: User preferences and configuration
- **Visualization Manager**: Chart generation and export
- **Module System**: Extensible plugin architecture

## Development

### Adding New Modules

1. **Create Module Class**

   ```python
   from core.base_module import BaseModule, ModuleInfo, InputField, OutputField

   class MyModule(BaseModule):
       def get_info(self) -> ModuleInfo:
           return ModuleInfo(
               name="My Module",
               version="1.0.0",
               description="Description of my module",
               category="Custom",
               author="Your Name",
               input_fields=[...],
               output_fields=[...],
               chart_types=[...]
           )

       def validate_inputs(self, inputs):
           # Validation logic
           pass

       def calculate(self, inputs):
           # Calculation logic
           pass
   ```

2. **Register Module**

   ```python
   # In calculation_engine.py
   from modules.custom.my_module import MyModule
   self.register_module(MyModule())
   ```

3. **Add to Module Directory**
   - Place module in `modules/custom/` directory
   - Update `__init__.py` files as needed

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculation_engine.py

# Run with coverage
pytest --cov=core --cov=modules --cov=gui
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed main.py

# Build with all dependencies
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

## Configuration

### Settings File

HeroCal uses `settings.json` for configuration:

```json
{
  "application": {
    "auto_save": true,
    "auto_save_interval": 300,
    "check_updates": true
  },
  "units": {
    "system": "SI",
    "length": "m",
    "force": "N"
  },
  "display": {
    "theme": "dark",
    "precision": 6
  }
}
```

### Environment Variables

- `HEROCAL_CONFIG_PATH`: Custom configuration file path
- `HEROCAL_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `HEROCAL_DATA_PATH`: Custom data directory path

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add unit tests for new features
- Update documentation as needed
- Use type hints for better code clarity

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Wiki](https://github.com/yourusername/herocal/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/herocal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/herocal/discussions)

## Roadmap

### Version 1.1

- [ ] Additional structural analysis modules
- [ ] AC circuit analysis
- [ ] 3D visualization capabilities
- [ ] Plugin marketplace

### Version 1.2

- [ ] Cloud synchronization
- [ ] Mobile companion app
- [ ] Advanced reporting features
- [ ] CAD integration

### Version 2.0

- [ ] Finite element analysis
- [ ] Machine learning integration
- [ ] Collaborative features
- [ ] Enterprise deployment tools

## Acknowledgments

- **PyQt6**: Cross-platform GUI framework
- **NumPy/SciPy**: Scientific computing libraries
- **Matplotlib**: Plotting and visualization
- **Engineering Community**: For feedback and suggestions

---

**HeroCal** - Making engineering calculations accessible, efficient, and professional.
