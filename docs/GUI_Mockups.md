# GUI Mockups and Design Specifications
## HeroCal - Engineering Calculator Application

---

## 1. Main Window Design

### 1.1 Main Application Window

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

### 1.2 Color Scheme and Styling

#### Dark Theme
- **Background**: #2b2b2b (Dark Gray)
- **Primary Panel**: #3c3c3c (Medium Gray)
- **Secondary Panel**: #4a4a4a (Light Gray)
- **Text**: #ffffff (White)
- **Accent**: #0078d4 (Blue)
- **Success**: #107c10 (Green)
- **Warning**: #ff8c00 (Orange)
- **Error**: #d13438 (Red)

#### Light Theme
- **Background**: #f5f5f5 (Light Gray)
- **Primary Panel**: #ffffff (White)
- **Secondary Panel**: #f0f0f0 (Very Light Gray)
- **Text**: #323130 (Dark Gray)
- **Accent**: #0078d4 (Blue)
- **Success**: #107c10 (Green)
- **Warning**: #ff8c00 (Orange)
- **Error**: #d13438 (Red)

---

## 2. Module Dialog Designs

### 2.1 Beam Analysis Dialog

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Beam Analysis Calculator                    [Min] [Max] [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│ Input Parameters                                                            │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Beam Properties                                                         │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Length (L):           [5.0        ] m                             │ │ │
│ │ │ Applied Load (P):     [1000       ] N                             │ │ │
│ │ │ Moment of Inertia:    [0.001      ] m⁴                            │ │ │
│ │ │ Modulus of Elasticity:[2e11       ] Pa                             │ │ │
│ │ │ Support Type:         [Simply Supported ▼]                         │ │ │
│ │ │ Load Position:        [2.5        ] m                             │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ │                                                                         │ │
│ │ Material Properties                                                     │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Material:            [Steel ▼]                                     │ │ │
│ │ │ Yield Strength:      [250e6        ] Pa                            │ │ │
│ │ │ Safety Factor:       [2.0          ]                               │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ Results                                                                      │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Maximum Deflection:   1.56 mm                                      │ │ │
│ │ │ Maximum Stress:       1.25 MPa                                     │ │ │
│ │ │ Left Reaction:        500 N                                        │ │ │
│ │ │ Right Reaction:       500 N                                        │ │ │
│ │ │ Safety Factor:        2.4                                          │ │ │
│ │ │ Status:               ✅ Safe                                      │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [Calculate] [Reset] [Export Results] [Show Chart] [Save to Project] [Close] │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Electrical Circuit Analysis Dialog

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  DC Circuit Analysis Calculator               [Min] [Max] [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│ Circuit Configuration                                                       │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Circuit Type:           [Series ▼]                                     │ │
│ │                                                                         │ │
│ │ Voltage Source:         [12.0        ] V                               │ │
│ │ Current:                [0.5         ] A                               │ │
│ │ Resistance:             [24.0        ] Ω                               │ │
│ │                                                                         │ │
│ │ Additional Components:                                                  │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ R1: [10.0] Ω  R2: [14.0] Ω  R3: [0.0] Ω  R4: [0.0] Ω              │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ Results                                                                      │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Total Resistance:      24.0 Ω                                      │ │ │
│ │ │ Total Current:         0.5 A                                       │ │ │
│ │ │ Total Voltage:         12.0 V                                      │ │ │
│ │ │ Power Dissipation:     6.0 W                                       │ │ │
│ │ │ Voltage Drop R1:       5.0 V                                       │ │ │
│ │ │ Voltage Drop R2:       7.0 V                                       │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [Calculate] [Reset] [Show Circuit Diagram] [Export Results] [Close]         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Settings Dialog

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Settings                        [Min] [Max] [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│ General          Units          Display        Advanced        About        │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Application Settings                                                    │ │
│ │                                                                         │ │
│ │ ☑ Auto-save projects                                                   │ │
│ │ Auto-save interval: [5] minutes                                        │ │
│ │                                                                         │ │
│ │ ☑ Check for updates on startup                                         │ │
│ │ ☑ Show tooltips                                                        │ │
│ │ ☑ Enable calculation history                                            │ │
│ │ ☑ Enable error reporting                                               │ │
│ │                                                                         │ │
│ │ Default project location:                                               │ │
│ │ [C:\Users\...\Documents\HeroCal\Projects    ] [Browse]                 │ │
│ │                                                                         │ │
│ │ Language: [English ▼]                                                  │ │
│ │                                                                         │ │
│ │ Calculation Settings                                                    │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Default precision: [6] decimal places                               │ │ │
│ │ │ Scientific notation threshold: [1e-3]                               │ │ │
│ │ │ Maximum calculation time: [30] seconds                              │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [OK] [Cancel] [Apply] [Reset to Defaults] [Import Settings] [Export Settings]│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Visualization Components

### 3.1 Chart Display Widget

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Beam Deflection Diagram                                    [Export] [Zoom] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    0.002 │                                                                    │
│          │                                                                    │
│    0.001 │        ●                                                          │
│          │       ╱ ╲                                                         │
│    0.000 │      ╱   ╲                                                        │
│          │     ╱     ╲                                                       │
│   -0.001 │    ╱       ╲                                                      │
│          │   ╱         ╲                                                     │
│   -0.002 │  ╱           ╲                                                    │
│          │ ╱             ╲                                                   │
│          └───────────────────────────────────────────────────────────────── │
│            0    1    2    3    4    5                                        │
│                    Position (m)                                              │
│                                                                             │
│ Legend:                                                                     │
│ ● Deflection (mm)                                                           │
│                                                                             │
│ [Show Grid] [Show Points] [Show Values] [Full Screen]                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Results Summary Panel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Results Summary                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ✅ Calculation Completed Successfully                                   │ │
│ │ Execution Time: 0.023 seconds                                          │ │
│ │                                                                         │ │
│ │ Key Results:                                                            │ │
│ │ • Maximum Deflection: 1.56 mm                                          │ │
│ │ • Maximum Stress: 1.25 MPa                                             │ │
│ │ • Safety Factor: 2.4 (Safe)                                            │ │
│ │                                                                         │ │
│ │ Warnings:                                                               │ │
│ │ • Deflection is close to limit (L/300 = 1.67 mm)                      │ │
│ │                                                                         │ │
│ │ Recommendations:                                                        │ │
│ │ • Consider increasing beam depth for better deflection control         │ │
│ │ • Current design is safe but could be optimized                        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [Copy Results] [Export to Report] [Save as Template]                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Navigation and Menu Design

### 4.1 Menu Bar Structure

```
File
├── New Project
├── Open Project...
├── Open Recent
│   ├── Project1.ecp
│   ├── Project2.ecp
│   └── Project3.ecp
├── ─────────────────
├── Save Project
├── Save Project As...
├── ─────────────────
├── Export
│   ├── Export to PDF...
│   ├── Export to Excel...
│   └── Export to CSV...
├── ─────────────────
├── Print...
├── ─────────────────
└── Exit

Edit
├── Undo
├── Redo
├── ─────────────────
├── Cut
├── Copy
├── Paste
├── ─────────────────
├── Find...
├── Replace...
├── ─────────────────
└── Preferences...

View
├── Toolbar
├── Status Bar
├── ─────────────────
├── Module Panel
├── Results Panel
├── Chart Panel
├── ─────────────────
├── Zoom In
├── Zoom Out
├── Fit to Window
├── ─────────────────
└── Full Screen

Modules
├── Structural
│   ├── Beam Analysis
│   ├── Column Analysis
│   └── Frame Analysis
├── Electrical
│   ├── DC Circuit Analysis
│   ├── AC Circuit Analysis
│   └── Power Analysis
├── Thermal
│   ├── Heat Transfer
│   ├── Ideal Gas Law
│   └── Efficiency Analysis
├── ─────────────────
├── Manage Modules...
└── Install Module...

Settings
├── General
├── Units
├── Display
├── Advanced
├── ─────────────────
├── Import Settings...
├── Export Settings...
└── Reset to Defaults

Help
├── User Manual
├── Tutorials
├── Examples
├── ─────────────────
├── Check for Updates
├── About HeroCal
└── ─────────────────
└── Report Bug
```

### 4.2 Toolbar Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [New] [Open] [Save] [Export] [Print] │ [Undo] [Redo] │ [Calculate] [Reset] │
│   📄    📁    💾    📤      🖨️      │   ↶     ↷     │     ⚡      🔄      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Responsive Design Considerations

### 5.1 Window Size Adaptations

#### Minimum Size (800x600)
- Hide secondary panels
- Collapse module list to icons
- Stack input and results vertically
- Minimize chart display

#### Standard Size (1200x800)
- Show all panels
- Full module list
- Side-by-side input and results
- Standard chart display

#### Large Size (1600x1000+)
- Expand chart display
- Show additional information panels
- Enable multi-chart display
- Show detailed calculation steps

### 5.2 Mobile/Tablet Adaptations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HeroCal - Engineering Calculator                            [☰] [Settings] │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Module: Beam Analysis ▼                                                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Input Parameters                                                        │ │
│ │ Length: [5.0] m                                                         │ │
│ │ Load: [1000] N                                                          │ │
│ │ Inertia: [0.001] m⁴                                                     │ │
│ │ Elasticity: [2e11] Pa                                                   │ │
│ │ Support: [Simply Supported ▼]                                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [Calculate]                                                                 │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Results                                                                 │ │
│ │ Max Deflection: 1.56 mm                                                 │ │
│ │ Max Stress: 1.25 MPa                                                    │ │
│ │ Safety Factor: 2.4                                                      │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [Show Chart] [Export] [Save]                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Accessibility Features

### 6.1 Keyboard Navigation
- **Tab**: Navigate between input fields
- **Enter**: Execute calculation
- **Escape**: Close dialogs
- **Ctrl+N**: New project
- **Ctrl+O**: Open project
- **Ctrl+S**: Save project
- **F1**: Help
- **F5**: Refresh/Recalculate

### 6.2 Screen Reader Support
- All UI elements have descriptive labels
- Charts include text descriptions
- Results are announced when calculations complete
- Status messages are spoken

### 6.3 High Contrast Mode
- Increased contrast ratios
- Larger fonts
- Simplified color palette
- Enhanced borders and outlines

---

## 7. Animation and Transitions

### 7.1 Smooth Transitions
- **Panel switching**: 200ms slide animation
- **Dialog opening**: 150ms fade-in
- **Chart updates**: 300ms smooth transition
- **Status changes**: 100ms color transition

### 7.2 Loading Indicators
- **Calculation progress**: Spinning indicator with percentage
- **File operations**: Progress bar with status text
- **Module loading**: Skeleton screens for better perceived performance

---

**Document Status**: ✅ **COMPLETE**  
**Next Phase**: Implementation  
**Approval**: Ready for Phase 3 Development
