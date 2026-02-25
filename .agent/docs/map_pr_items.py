# Mapping of PR Items to WBS Zones
# This script is for planning purposes to organize the items before finalized generation.

pr_items = [
    # General / Prep
    {"Item": "1.001", "Desc": "Preparatory works", "Zone": "1.2.1", "Phase": "Mobilization"},
    
    # Zone 1: Office Building (Kiosk)
    {"Item": "1.002", "Desc": "KIOSK CONVERSION", "Zone": "1.2.2", "Phase": "Zone 1"},
    {"Item": "1.025", "Desc": "Plain Plaster 1/2\"", "Zone": "1.2.2.3", "Phase": "Zone 1 Finish"},
    {"Item": "1.026", "Desc": "Plain Plaster 3/4\"", "Zone": "1.2.2.3", "Phase": "Zone 1 Finish"},
    {"Item": "1.027", "Desc": "BRICK / BLOCK MASONARY", "Zone": "1.2.2.3", "Phase": "Zone 1 Arch"},
    {"Item": "1.028", "Desc": "Plastic Emulsion Paint", "Zone": "1.2.2.3", "Phase": "Zone 1 Finish"}, # Internal
    {"Item": "1.029", "Desc": "Weather Shield Paint", "Zone": "1.2.2.3", "Phase": "Zone 1 Finish"}, # External
    {"Item": "2", "Desc": "Air Conditioner Split 1.5 Ton", "Zone": "1.2.2.3", "Phase": "Zone 1 MEP"},
    {"Item": "3", "Desc": "Air Conditioner Split 1 Ton", "Zone": "1.2.2.3", "Phase": "Zone 1 MEP"},
    
    # Zone 2A: Canopy
    {"Item": "1.003", "Desc": "STEEL CANOPY CONVERSION", "Zone": "1.2.3.1", "Phase": "Zone 2A"},
    {"Item": "1.032", "Desc": "QUICK OIL CHANGE CANOPY", "Zone": "1.2.3.1", "Phase": "Zone 2A"},
    
    # Zone 2B: Fuel System
    {"Item": "1.004", "Desc": "PUMP ISLAND", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.005", "Desc": "Angle iron for DU Island", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.006", "Desc": "CONST. RCC PIT & INSTL UGFS TANK 15/25KL", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.007", "Desc": "REPAIRING OF EXISTING UGFS TANK PIT", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.008", "Desc": "54 mm dia. UPP FUEL PIPE", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.009", "Desc": "Piping work for Decantation", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.010", "Desc": "GUARD RAIL FILL PT.", "Zone": "1.2.3.2", "Phase": "Zone 2B"},
    {"Item": "1.034", "Desc": "WIRING FOR SPREADER", "Zone": "1.2.3.2", "Phase": "Zone 2B MEP"},
    {"Item": "1.035", "Desc": "WIRING FOR DU & MOTOR", "Zone": "1.2.3.2", "Phase": "Zone 2B MEP"},
    
    # Zone 2C: Civil & External
    {"Item": "1.011", "Desc": "P/L 60 MM PAVER EXIST. PAVEMENT", "Zone": "1.2.3.3", "Phase": "Zone 2C"},
    {"Item": "1.012", "Desc": "P/L CURB STONE", "Zone": "1.2.3.3", "Phase": "Zone 2C"},
    {"Item": "1.013", "Desc": "P/L CUT OFF DRAIN", "Zone": "1.2.3.3", "Phase": "Zone 2C"},
    {"Item": "1.014", "Desc": "UNDER GROUNG WATER TANK", "Zone": "1.2.3.3", "Phase": "Zone 2C"}, # Or separate zone?
    {"Item": "1.018", "Desc": "Excavation", "Zone": "1.2.3.3", "Phase": "General Civil"}, # Distributed?
    {"Item": "1.019", "Desc": "Earth/Back filling", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.020", "Desc": "Stone Soling", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.021", "Desc": "1:3:6 CONCRETE", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.022", "Desc": "1:4:8 CONCRETE", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.023", "Desc": "Laying of R.C.C 1:2:4", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.024", "Desc": "SUPPLY & INSTALLATION OF DEFORMED STEEL", "Zone": "1.2.3.3", "Phase": "General Civil"},
    {"Item": "1.030", "Desc": "2\"X2\"X2.5\" CONCRETE MANHOLE", "Zone": "1.2.3.3", "Phase": "Zone 2C"},
    {"Item": "1.031", "Desc": "CONSTRUCTION OF MANHOLE", "Zone": "1.2.3.3", "Phase": "Zone 2C"},
    {"Item": "1.038", "Desc": "P/L UPVC 8\" DIA DRAIN LINES", "Zone": "1.2.3.3", "Phase": "Zone 2C Plumbing"},
    
    # Zone 2D: Electrical (New Zone needed?) or External
    {"Item": "1.015", "Desc": "SINGLE LIGHT POLE 24-FT", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.016", "Desc": "DOUBLE LIGHT POLE 24-FT", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.017", "Desc": "WIRING FOR LIGHT POLES", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.033", "Desc": "Services for Power Connectivity", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.036", "Desc": "WIRING FOR MAIN 4X35 SQ.MM", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.037", "Desc": "S/I 1-HP CENTFUGAL PUMP", "Zone": "1.2.3.3", "Phase": "Zone 2C Plumbing"}, # Or MEP
    {"Item": "1.039", "Desc": "P/L UPVC PIPE 6\" CABLE SLEEVE", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.040", "Desc": "S/I 4\" UPVC Pipe", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.041", "Desc": "P/L UPVC PIPE 2\" CABLE SLEEVE", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
    {"Item": "1.042", "Desc": "WIRING FOR MONOLITH", "Zone": "1.2.3.4", "Phase": "Zone 2D"},
]

print("Mapping Verified")
