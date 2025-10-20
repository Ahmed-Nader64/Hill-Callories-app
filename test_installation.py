#!/usr/bin/env python3
"""
Test script to verify HeroCal installation and dependencies.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'PyQt6',
        'numpy',
        'scipy',
        'matplotlib',
        'sympy',
        'plotly',
        'reportlab',
        'openpyxl'
    ]
    
    print("Testing required module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies using:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required modules imported successfully!")
        return True

def test_core_modules():
    """Test if core HeroCal modules can be imported"""
    print("\nTesting HeroCal core modules...")
    
    try:
        from core.base_module import BaseModule, ModuleInfo, InputField, OutputField
        print("✅ Core base module")
    except ImportError as e:
        print(f"❌ Core base module: {e}")
        return False
    
    try:
        from core.calculation_engine import CalculationEngine
        print("✅ Calculation engine")
    except ImportError as e:
        print(f"❌ Calculation engine: {e}")
        return False
    
    try:
        from core.data_manager import DataManager
        print("✅ Data manager")
    except ImportError as e:
        print(f"❌ Data manager: {e}")
        return False
    
    try:
        from core.settings_manager import SettingsManager
        print("✅ Settings manager")
    except ImportError as e:
        print(f"❌ Settings manager: {e}")
        return False
    
    try:
        from core.visualization_manager import VisualizationManager
        print("✅ Visualization manager")
    except ImportError as e:
        print(f"❌ Visualization manager: {e}")
        return False
    
    return True

def test_engineering_modules():
    """Test if engineering modules can be imported"""
    print("\nTesting engineering modules...")
    
    try:
        from modules.structural.beam_analysis import BeamAnalysis
        print("✅ Beam analysis module")
    except ImportError as e:
        print(f"❌ Beam analysis module: {e}")
        return False
    
    try:
        from modules.electrical.dc_circuit import DCCircuitAnalysis
        print("✅ DC circuit analysis module")
    except ImportError as e:
        print(f"❌ DC circuit analysis module: {e}")
        return False
    
    try:
        from modules.thermal.heat_transfer import HeatTransferAnalysis
        print("✅ Heat transfer analysis module")
    except ImportError as e:
        print(f"❌ Heat transfer analysis module: {e}")
        return False
    
    return True

def test_gui_modules():
    """Test if GUI modules can be imported"""
    print("\nTesting GUI modules...")
    
    try:
        from gui.main_window import MainWindow
        print("✅ Main window")
    except ImportError as e:
        print(f"❌ Main window: {e}")
        return False
    
    try:
        from gui.module_panel import ModulePanel
        print("✅ Module panel")
    except ImportError as e:
        print(f"❌ Module panel: {e}")
        return False
    
    try:
        from gui.input_panel import InputPanel
        print("✅ Input panel")
    except ImportError as e:
        print(f"❌ Input panel: {e}")
        return False
    
    try:
        from gui.results_panel import ResultsPanel
        print("✅ Results panel")
    except ImportError as e:
        print(f"❌ Results panel: {e}")
        return False
    
    try:
        from gui.visualization_panel import VisualizationPanel
        print("✅ Visualization panel")
    except ImportError as e:
        print(f"❌ Visualization panel: {e}")
        return False
    
    return True

def test_calculation_engine():
    """Test if calculation engine can be instantiated and modules loaded"""
    print("\nTesting calculation engine functionality...")
    
    try:
        from core.calculation_engine import CalculationEngine
        engine = CalculationEngine()
        
        # Test module loading
        modules = engine.get_available_modules()
        print(f"✅ Loaded {len(modules)} modules: {', '.join(modules)}")
        
        # Test module categories
        categories = engine.get_module_categories()
        print(f"✅ Module categories: {', '.join(categories.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Calculation engine test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("HeroCal Installation Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test external dependencies
    if not test_imports():
        all_tests_passed = False
    
    # Test core modules
    if not test_core_modules():
        all_tests_passed = False
    
    # Test engineering modules
    if not test_engineering_modules():
        all_tests_passed = False
    
    # Test GUI modules
    if not test_gui_modules():
        all_tests_passed = False
    
    # Test calculation engine
    if not test_calculation_engine():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! HeroCal is ready to use.")
        print("\nTo start the application, run:")
        print("python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
