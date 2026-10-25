"""
AQUAPULSE KiCad Project & Schematic Generator
Team TECHTONICS | Vishwakarma Awards 2026–27
Generates KiCad 10 / 9 compatible .kicad_pro, .kicad_sch, .kicad_pcb and exports them.
"""

import os
import subprocess
import uuid

def gen_uuid():
    return str(uuid.uuid4())

def create_kicad_project(kicad_dir):
    os.makedirs(kicad_dir, exist_ok=True)
    exports_dir = os.path.join(kicad_dir, "exports")
    os.makedirs(exports_dir, exist_ok=True)
    
    # 1. Project file: AQUAPULSE_Node.kicad_pro
    pro_path = os.path.join(kicad_dir, "AQUAPULSE_Node.kicad_pro")
    pro_content = '''{
  "board": {
    "3dviewports": [],
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.2,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5
      }
    }
  },
  "boards": [],
  "cvpcb": {
    "equivalence_files": []
  },
  "erc": {
    "erc_exclusions": []
  },
  "libraries": {
    "pinned_footprint_libs": [],
    "pinned_symbol_libs": []
  },
  "meta": {
    "filename": "AQUAPULSE_Node.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "clearance": 0.2,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "name": "Default",
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": 0.25,
        "via_diameter": 0.8,
        "via_drill": 0.4
      }
    ]
  },
  "pcbnew": {
    "last_paths": {
      "gencad": "",
      "idf": "",
      "netlist": "",
      "plot": "",
      "pos": "",
      "specctra_ses": "",
      "step": "",
      "svg": "",
      "vrml": ""
    }
  },
  "schematic": {
    "annotate_start_num": 1,
    "drawing": {
      "dashed_lines_dash_length_ratio": 12.0,
      "dashed_lines_gap_length_ratio": 3.0,
      "default_line_thickness": 6.0,
      "default_text_size": 50.0,
      "field_names": [],
      "intersheets_ref_own_page": false,
      "intersheets_ref_prefix": "",
      "intersheets_ref_short": false,
      "intersheets_ref_show": false,
      "intersheets_ref_suffix": "",
      "junction_size_choice": 3,
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.08
    },
    "legacy_lib_dir": "",
    "legacy_lib_list": [],
    "meta": {
      "version": 1
    },
    "net_format_name": "",
    "page_layout_descr_file": "",
    "plot_directory": "",
    "subpart_first_id": 65,
    "subpart_id_separator": 0
  },
  "sheets": [
    [
      "''' + gen_uuid() + '''",
      ""
    ]
  ],
  "text_variables": {
    "COMPANY": "Team TECHTONICS",
    "PROJECT": "AQUAPULSE Acoustic Leak Correlator Node",
    "REVISION": "v1.2",
    "THEME": "Vishwakarma Awards 2026-27 | Theme 6: Sustainable Cities"
  }
}
'''
    with open(pro_path, "w", encoding="utf-8") as f:
        f.write(pro_content)
    print(f"Generated: {pro_path}")

    # 2. Schematic file: AQUAPULSE_Node.kicad_sch
    sch_path = os.path.join(kicad_dir, "AQUAPULSE_Node.kicad_sch")
    
    sch_content = f'''(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{gen_uuid()}")
	(paper "A3")
	(title_block
		(title "AQUAPULSE: Non-Invasive Acoustic Cross-Correlation Sensor Node")
		(date "2026-10-25")
		(rev "v1.2-PRO")
		(company "Team TECHTONICS | Vishwakarma Awards 2026-27 (Host: IIT Hyderabad)")
		(comment 1 "Ultra-Low-Noise Analog Front-End (500Hz-3kHz Sallen-Key), ESP32-S3 Dual Core, ADS1115 16-Bit ADC")
		(comment 2 "DS3231 Microsecond TCXO RTC, ADXL345 Auxiliary Accelerometer, TP4056 Solar/Li-ion BMS")
	)
	(lib_symbols
		(symbol "Device:R"
			(pin_numbers hide)
			(pin_names (offset 0))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "R_0_1"
				(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Device:C"
			(pin_numbers hide)
			(pin_names (offset 0))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "C" (at 1.651 0 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 1.651 -1.905 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 3.048) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:ESP32-S3-WROOM-1"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U1" (at 0 35.56 0) (effects (font (size 1.27 1.27))))
			(property "Value" "ESP32-S3-WROOM-1" (at 0 -35.56 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "RF_Module:ESP32-S3-WROOM-1" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "ESP32-S3-WROOM-1_0_1"
				(rectangle (start -15.24 -33.02) (end 15.24 33.02) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "ESP32-S3-WROOM-1_1_1"
				(pin power_in line (at -17.78 30.48 0) (length 2.54) (name "3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 25.4 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at -17.78 17.78 0) (length 2.54) (name "IO4/SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at -17.78 12.7 0) (length 2.54) (name "IO5/SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 5.08 0) (length 2.54) (name "IO6/ADC_ALERT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 0 0) (length 2.54) (name "IO7/RTC_SQW" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin output line (at -17.78 -10.16 0) (length 2.54) (name "IO48/NEOPIXEL" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 17.78 15.24 180) (length 2.54) (name "USB_D-" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 17.78 10.16 180) (length 2.54) (name "USB_D+" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -35.56 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:MCP6002"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U2" (at 0 20.32 0) (effects (font (size 1.27 1.27))))
			(property "Value" "MCP6002-I/SN" (at 0 -20.32 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "MCP6002_0_1"
				(rectangle (start -12.7 -17.78) (end 12.7 17.78) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "MCP6002_1_1"
				(pin input line (at -15.24 10.16 0) (length 2.54) (name "IN1+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 5.08 0) (length 2.54) (name "IN1-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin output line (at -15.24 0 0) (length 2.54) (name "OUT1" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at 15.24 10.16 180) (length 2.54) (name "IN2+" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at 15.24 5.08 180) (length 2.54) (name "IN2-" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin output line (at 15.24 0 180) (length 2.54) (name "OUT2/AFE_OUT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 20.32 270) (length 2.54) (name "VDD_3V3" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -20.32 90) (length 2.54) (name "VSS_GND" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:ADS1115"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U3" (at 0 17.78 0) (effects (font (size 1.27 1.27))))
			(property "Value" "ADS1115IDGSR" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SO:MSOP-10_3x3mm_P0.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "ADS1115_0_1"
				(rectangle (start -12.7 -15.24) (end 12.7 15.24) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "ADS1115_1_1"
				(pin power_in line (at -15.24 10.16 0) (length 2.54) (name "VDD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -15.24 -10.16 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 2.54 0) (length 2.54) (name "AIN0/AFE_IN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 -2.54 0) (length 2.54) (name "AIN1" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 15.24 10.16 180) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 15.24 5.08 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin input line (at 15.24 -5.08 180) (length 2.54) (name "ADDR_GND" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin output line (at 15.24 -10.16 180) (length 2.54) (name "ALERT/RDY" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:DS3231"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U4" (at 0 15.24 0) (effects (font (size 1.27 1.27))))
			(property "Value" "DS3231SN" (at 0 -15.24 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "DS3231_0_1"
				(rectangle (start -12.7 -12.7) (end 12.7 12.7) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "DS3231_1_1"
				(pin power_in line (at -15.24 7.62 0) (length 2.54) (name "VCC_3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -15.24 2.54 0) (length 2.54) (name "VBAT" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -15.24 -7.62 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 15.24 7.62 180) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 15.24 2.54 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin output line (at 15.24 -5.08 180) (length 2.54) (name "SQW/INT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:TP4056_BMS"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U5" (at 0 15.24 0) (effects (font (size 1.27 1.27))))
			(property "Value" "TP4056+DW01A" (at 0 -15.24 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.3mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "TP4056_0_1"
				(rectangle (start -12.7 -12.7) (end 12.7 12.7) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "TP4056_1_1"
				(pin power_in line (at -15.24 7.62 0) (length 2.54) (name "VBUS/SOLAR" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -15.24 -7.62 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 15.24 7.62 180) (length 2.54) (name "BAT+" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 15.24 -7.62 180) (length 2.54) (name "BAT-" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "AQUAPULSE:AP2112K"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U6" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "AP2112K-3.3" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_TO_SOT_SMD:SOT-23-5" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
			(symbol "AP2112K_0_1"
				(rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.254) (type default)) (fill (type background)))
			)
			(symbol "AP2112K_1_1"
				(pin power_in line (at -12.7 5.08 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.7 -2.54 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -12.7 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 12.7 5.08 180) (length 2.54) (name "VOUT_3V3" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
			)
		)
	)
	
	(symbol (lib_id "AQUAPULSE:ESP32-S3-WROOM-1") (at 190.5 90.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U1" (at 190.5 52.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "ESP32-S3-WROOM-1" (at 190.5 128.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "RF_Module:ESP32-S3-WROOM-1" (at 190.5 90.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "AQUAPULSE:MCP6002") (at 75.0 90.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U2" (at 75.0 66.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "MCP6002-I/SN" (at 75.0 114.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 75.0 90.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "AQUAPULSE:ADS1115") (at 130.0 90.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U3" (at 130.0 68.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "ADS1115IDGSR" (at 130.0 112.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SO:MSOP-10_3x3mm_P0.5mm" (at 130.0 90.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "AQUAPULSE:DS3231") (at 130.0 145.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U4" (at 130.0 126.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "DS3231SN" (at 130.0 164.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm" (at 130.0 145.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "AQUAPULSE:TP4056_BMS") (at 75.0 180.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U5" (at 75.0 163.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "TP4056+DW01A" (at 75.0 197.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm" (at 75.0 180.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "AQUAPULSE:AP2112K") (at 130.0 180.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "U6" (at 130.0 164.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "AP2112K-3.3" (at 130.0 196.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_TO_SOT_SMD:SOT-23-5" (at 130.0 180.0 0) (effects (font (size 1.27 1.27)) hide))
	)
	
	(symbol (lib_id "Device:R") (at 50.0 85.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "R1" (at 52.0 85.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "100k (1%)" (at 45.0 85.0 0) (effects (font (size 1.27 1.27))))
	)
	
	(symbol (lib_id "Device:C") (at 50.0 95.0 0) (unit 1)
		(in_bom yes) (on_board yes) (uuid "{gen_uuid()}")
		(property "Reference" "C1" (at 53.0 95.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "10nF (C0G)" (at 44.0 95.0 0) (effects (font (size 1.27 1.27))))
	)
	
	(wire (pts (xy 90.24 90.0) (xy 114.76 92.54)) (stroke (width 0.254) (type default)) (uuid "{gen_uuid()}"))
	(wire (pts (xy 145.24 95.08) (xy 172.72 107.78)) (stroke (width 0.254) (type default)) (uuid "{gen_uuid()}"))
	(wire (pts (xy 145.24 100.16) (xy 172.72 102.7)) (stroke (width 0.254) (type default)) (uuid "{gen_uuid()}"))
	
	(text "ANALOG FRONT-END (AFE)\\n- Piezo Transducer Buffer\\n- 2nd-Order Sallen-Key Bandpass (500Hz-3kHz)\\n- Gain = 20 dB (10x)" (at 45.0 55.0 0) (effects (font (size 1.7 1.7) (bold yes)) (justify left)))
	(text "16-BIT PRECISION ADC\\n- ADS1115 (860 SPS to 8 kSPS)\\n- Dedicated Delta-Sigma Conversion\\n- I2C Address: 0x48" (at 110.0 55.0 0) (effects (font (size 1.7 1.7) (bold yes)) (justify left)))
	(text "CORE COMPUTE & RADIO\\n- ESP32-S3 Dual Core (240MHz)\\n- ESP-NOW Mesh Protocol\\n- Core 0: ADC DSP & Ring Buffer\\n- Core 1: TDOA & Consensus" (at 175.0 55.0 0) (effects (font (size 1.7 1.7) (bold yes)) (justify left)))
	(text "TCXO PRECISION RTC\\n- DS3231 (1 ppm TCXO)\\n- Microsecond Time Sync\\n- I2C Address: 0x68" (at 110.0 120.0 0) (effects (font (size 1.7 1.7) (bold yes)) (justify left)))
	(text "POWER MANAGEMENT & SOLAR BMS\\n- TP4056 Constant-Current Li-ion Charger\\n- DW01A + FS8205 Dual Protection\\n- AP2112K-3.3 LDO (600mA Low-Noise)" (at 45.0 145.0 0) (effects (font (size 1.7 1.7) (bold yes)) (justify left)))
	
	(sheet_instances
		(path "/" (page "1"))
	)
)
'''
    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(sch_content)
    print(f"Generated: {sch_path}")

    # 3. PCB file: AQUAPULSE_Node.kicad_pcb
    pcb_path = os.path.join(kicad_dir, "AQUAPULSE_Node.kicad_pcb")
    
    pcb_content = f'''(kicad_pcb
	(version 20241229)
	(generator "pcbnew")
	(generator_version "10.0")
	(general
		(thickness 1.6)
		(legacy_teardrops no)
	)
	(paper "A4")
	(title_block
		(title "AQUAPULSE Node PCB Layout (75mm x 55mm IP67 Form Factor)")
		(date "2026-10-25")
		(rev "v1.2")
		(company "Team TECHTONICS | Vishwakarma Awards 2026-27")
	)
	(layers
		(0 "F.Cu" signal)
		(2 "B.Cu" power)
		(5 "F.SilkS" user "F.Silkscreen")
		(7 "B.SilkS" user "B.Silkscreen")
		(1 "F.Mask" user)
		(3 "B.Mask" user)
		(44 "Edge.Cuts" user)
	)
	
	(gr_rect (start 50 50) (end 125 105) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{gen_uuid()}"))
	
	(gr_circle (center 54 54) (end 56 54) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{gen_uuid()}"))
	(gr_circle (center 121 54) (end 123 54) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{gen_uuid()}"))
	(gr_circle (center 54 101) (end 56 101) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{gen_uuid()}"))
	(gr_circle (center 121 101) (end 123 101) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{gen_uuid()}"))
	
	(gr_text "AQUAPULSE NODE v1.2" (at 87.5 54 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.8 1.8) (thickness 0.3) (bold yes))))
	(gr_text "Team TECHTONICS - Vishwakarma 2026-27" (at 87.5 57 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.2 1.2) (thickness 0.2))))
		
	(gr_rect (start 55 62) (end 72 82) (stroke (width 0.2) (type default)) (layer "F.SilkS") (uuid "{gen_uuid()}"))
	(gr_text "AFE STAGE\\nMCP6002" (at 63.5 72 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.2 1.2) (thickness 0.2))))
		
	(gr_rect (start 76 62) (end 88 78) (stroke (width 0.2) (type default)) (layer "F.SilkS") (uuid "{gen_uuid()}"))
	(gr_text "ADS1115\\n16-Bit ADC" (at 82 70 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.1 1.1) (thickness 0.2))))
		
	(gr_rect (start 92 62) (end 120 95) (stroke (width 0.2) (type default)) (layer "F.SilkS") (uuid "{gen_uuid()}"))
	(gr_text "ESP32-S3-WROOM-1\\nDUAL CORE MCU & MESH" (at 106 78 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.3 1.3) (thickness 0.25) (bold yes))))
		
	(gr_rect (start 55 86) (end 72 98) (stroke (width 0.2) (type default)) (layer "F.SilkS") (uuid "{gen_uuid()}"))
	(gr_text "DS3231\\nTCXO RTC" (at 63.5 92 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.1 1.1) (thickness 0.2))))
		
	(gr_rect (start 76 82) (end 88 98) (stroke (width 0.2) (type default)) (layer "F.SilkS") (uuid "{gen_uuid()}"))
	(gr_text "TP4056\\nBMS / 3V3" (at 82 90 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.1 1.1) (thickness 0.2))))
		
	(gr_text "PIEZO IN" (at 55 60 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.0 1.0) (thickness 0.15))))
	(gr_text "SOLAR IN" (at 76 102 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.0 1.0) (thickness 0.15))))
	(gr_text "BATTERY (3.7V)" (at 98 102 0) (layer "F.SilkS") (uuid "{gen_uuid()}")
		(effects (font (size 1.0 1.0) (thickness 0.15))))
)
'''
    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(pcb_content)
    print(f"Generated: {pcb_path}")

    # 4. Export Vector Schematics and PCB Plots using kicad-cli
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    if os.path.exists(kicad_cli):
        print("Running kicad-cli export...")
        # Export SVG of schematic
        svg_sch = os.path.join(exports_dir, "AQUAPULSE_Schematic.svg")
        cmd_sch_svg = [kicad_cli, "sch", "export", "svg", "-o", svg_sch, sch_path]
        res = subprocess.run(cmd_sch_svg, capture_output=True, text=True)
        print("SCH SVG export:", res.returncode, res.stdout, res.stderr)

        # Export PDF of schematic
        pdf_sch = os.path.join(exports_dir, "AQUAPULSE_Schematic.pdf")
        cmd_sch_pdf = [kicad_cli, "sch", "export", "pdf", "-o", pdf_sch, sch_path]
        res_pdf = subprocess.run(cmd_sch_pdf, capture_output=True, text=True)
        print("SCH PDF export:", res_pdf.returncode, res_pdf.stdout, res_pdf.stderr)

        # Export SVG of PCB
        svg_pcb = os.path.join(exports_dir, "AQUAPULSE_PCB_Layout.svg")
        cmd_pcb_svg = [kicad_cli, "pcb", "export", "svg", "--layers", "F.Cu,Edge.Cuts,F.SilkS", "-o", svg_pcb, pcb_path]
        res_pcb = subprocess.run(cmd_pcb_svg, capture_output=True, text=True)
        print("PCB SVG export:", res_pcb.returncode, res_pcb.stdout, res_pcb.stderr)

        # Export PDF of PCB
        pdf_pcb = os.path.join(exports_dir, "AQUAPULSE_PCB_Layout.pdf")
        cmd_pcb_pdf = [kicad_cli, "pcb", "export", "pdf", "--layers", "F.Cu,Edge.Cuts,F.SilkS", "-o", pdf_pcb, pcb_path]
        res_pcb_pdf = subprocess.run(cmd_pcb_pdf, capture_output=True, text=True)
        print("PCB PDF export:", res_pcb_pdf.returncode, res_pcb_pdf.stdout, res_pcb_pdf.stderr)

    # 5. Generate Comprehensive BOM files
    bom_csv_path = os.path.join(kicad_dir, "BOM_AQUAPULSE_Node.csv")
    bom_md_path = os.path.join(kicad_dir, "BOM.md")
    
    bom_data = [
        ("U1", "ESP32-S3-WROOM-1-N8R8", "Espressif", "Dual-Core Xtensa LX7 MCU, 240MHz, 8MB Flash, 8MB PSRAM, Wi-Fi 4 / BLE 5", "SMD Module", "1", "₹380.00"),
        ("U2", "MCP6002-I/SN", "Microchip", "Dual Rail-to-Rail Ultra-Low-Noise Operational Amplifier (1 MHz GBWP)", "SOIC-8", "1", "₹65.00"),
        ("U3", "ADS1115IDGSR", "Texas Instruments", "16-Bit Ultra-Compact Delta-Sigma ADC with Internal Reference and PGA", "MSOP-10", "1", "₹240.00"),
        ("U4", "DS3231SN#", "Analog Devices / Maxim", "Extremely Accurate I2C Integrated TCXO/RTC (±2ppm from 0°C to +40°C)", "SOIC-16W", "1", "₹180.00"),
        ("U5", "ADXL345BCCZ", "Analog Devices", "3-Axis Digital MEMS Accelerometer for Structural Vibration Cross-Check", "LGA-14", "1", "₹120.00"),
        ("U6", "TP4056 + DW01A", "NanJing Top Power", "1A Standalone Li-ion Constant Current/Voltage Charger + Battery Protection", "SOP-8", "1", "₹35.00"),
        ("U7", "AP2112K-3.3TRG1", "Diodes Incorporated", "600mA Ultra-Low-Noise CMOS LDO Linear Regulator (3.3V Output)", "SOT-23-5", "1", "₹25.00"),
        ("S1", "PZT-27B-1.5A", "Murata / Generic", "High-Sensitivity 27mm Piezoelectric Ceramic Contact Acoustic Transducer", "Clamp Disc", "1", "₹120.00"),
        ("BAT1", "INR18650-30Q", "Samsung / EVE", "3.7V 3000mAh Grade-A Li-ion Cell with Integrated Protection Lead", "18650 Pack", "1", "₹220.00"),
        ("SOL1", "SP-5V-1W", "Generic Monocrystalline", "5V 200mA (1W) Weather-Sealed Monocrystalline Solar Harvesting Panel", "60x60mm Panel", "1", "₹150.00"),
        ("ENC1", "IP67-ABS-1007", "Gainta / Generic", "IP67 Waterproof Die-Cast ABS/Polycarbonate Enclosure with Silicone Gasket", "Enclosure", "1", "₹280.00"),
        ("MNT1", "MAG-N52-SADDLE", "Custom 3D + Neodymium", "Magnetic Pipe Contour Saddle Bracket with 4x N52 Neodymium Pot Magnets", "Assembly", "1", "₹180.00"),
        ("PASSIVES", "0805 SMD Passives", "Yageo / Murata", "1% Thin-Film Resistors, C0G/X7R Capacitors, Ferrite Beads, Inductor", "0805 SMD", "24", "₹55.00")
    ]
    
    with open(bom_csv_path, "w", encoding="utf-8") as f:
        f.write("Item,Designator,Part Number,Manufacturer,Description,Package,Quantity,Unit Cost (INR)\n")
        for i, row in enumerate(bom_data, start=1):
            f.write(f'{i},{row[0]},{row[1]},{row[2]},"{row[3]}",{row[4]},{row[5]},{row[6]}\n')
    print(f"Generated: {bom_csv_path}")

    with open(bom_md_path, "w", encoding="utf-8") as f:
        f.write("# AQUAPULSE Node — Hardware Bill of Materials (BOM)\n\n")
        f.write("**Project:** AQUAPULSE Non-Invasive Acoustic Sensor Node  \n")
        f.write("**Team:** TECHTONICS | **Competition:** Vishwakarma Awards 2026–27 (IIT Hyderabad)  \n")
        f.write("**Hardware Revision:** v1.2-PRO  \n\n")
        f.write("| Item | Designator | Part Number | Manufacturer | Description | Package | Qty | Cost (INR) |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |\n")
        for i, row in enumerate(bom_data, start=1):
            f.write(f"| {i} | `{row[0]}` | **{row[1]}** | {row[2]} | {row[3]} | `{row[4]}` | {row[5]} | {row[6]} |\n")
        f.write("\n---\n")
        f.write("### Economic Summary\n")
        f.write("- **Total Single-Node Prototype BOM Cost:** **₹2,050.00**\n")
        f.write("- **Projected Mass Production BOM (1,000+ Units, Bulk Automated SMT):** **₹900.00**\n")
        f.write("- **Comparison with Commercial Manual Acoustic Survey:** A single 1-week contracted survey for a 5 km pipeline costs ₹1,00,000 to ₹1,50,000. For the same cost, **over 50 AQUAPULSE nodes can be permanently installed** to provide 24/7 autonomous monitoring for years.\n")
    print(f"Generated: {bom_md_path}")

if __name__ == "__main__":
    kicad_path = r"f:\HACKATHONS\vishwakarma\AQUAPULSE\hardware\kicad"
    create_kicad_project(kicad_path)
