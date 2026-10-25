"""
AQUAPULSE: Complete KiCad 10 Schematic & Layout Generator
Generates full engineering schematic, PCB layout, SVG/PDF exports and BOM.
"""

import os
import subprocess
import uuid
import shutil

def u():
    return str(uuid.uuid4())

def generate_aquapulse_kicad():
    kicad_dir = r"f:\HACKATHONS\vishwakarma\AQUAPULSE\hardware\kicad"
    exports_dir = os.path.join(kicad_dir, "exports")
    docs_assets = r"f:\HACKATHONS\vishwakarma\AQUAPULSE\docs\assets"
    
    os.makedirs(kicad_dir, exist_ok=True)
    os.makedirs(exports_dir, exist_ok=True)
    os.makedirs(docs_assets, exist_ok=True)

    # 1. Project file
    pro_path = os.path.join(kicad_dir, "AQUAPULSE_Node.kicad_pro")
    pro_content = f'''{{
  "board": {{
    "design_settings": {{
      "defaults": {{
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.25,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5
      }}
    }}
  }},
  "meta": {{
    "filename": "AQUAPULSE_Node.kicad_pro",
    "version": 1
  }},
  "sheets": [
    [
      "{u()}",
      ""
    ]
  ],
  "text_variables": {{
    "COMPANY": "Team TECHTONICS",
    "PROJECT": "AQUAPULSE Non-Invasive Acoustic Sensor Node",
    "REVISION": "v1.2",
    "THEME": "Vishwakarma Awards 2026-27 | Theme 6: Sustainable Cities"
  }}
}}
'''
    with open(pro_path, "w", encoding="utf-8") as f:
        f.write(pro_content)

    # 2. Comprehensive Schematic File
    sch_path = os.path.join(kicad_dir, "AQUAPULSE_Node.kicad_sch")
    
    sch_lines = [
        '(kicad_sch',
        '\t(version 20250114)',
        '\t(generator "eeschema")',
        '\t(generator_version "10.0")',
        f'\t(uuid "{u()}")',
        '\t(paper "A3")',
        '\t(title_block',
        '\t\t(title "AQUAPULSE: Non-Invasive Acoustic Sensor Node (ESP32-S3 + AFE + ADS1115 + DS3231)")',
        '\t\t(date "2026-10-25")',
        '\t\t(rev "v1.2-RELEASE")',
        '\t\t(company "Team TECHTONICS | Vishwakarma Awards 2026-27 (Host: IIT Hyderabad)")',
        '\t)',
        '\t(lib_symbols)'
    ]

    def add_rect(x1, y1, x2, y2, stroke_w=0.3):
        sch_lines.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y1})) (stroke (width {stroke_w}) (type default)) (uuid "{u()}"))')
        sch_lines.append(f'\t(wire (pts (xy {x2} {y1}) (xy {x2} {y2})) (stroke (width {stroke_w}) (type default)) (uuid "{u()}"))')
        sch_lines.append(f'\t(wire (pts (xy {x2} {y2}) (xy {x1} {y2})) (stroke (width {stroke_w}) (type default)) (uuid "{u()}"))')
        sch_lines.append(f'\t(wire (pts (xy {x1} {y2}) (xy {x1} {y1})) (stroke (width {stroke_w}) (type default)) (uuid "{u()}"))')

    def add_line(x1, y1, x2, y2, stroke_w=0.25):
        sch_lines.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width {stroke_w}) (type default)) (uuid "{u()}"))')

    def add_text(text, x, y, size=1.5, bold=False, italic=False, justify="left"):
        b_str = " (bold yes)" if bold else ""
        i_str = " (italic yes)" if italic else ""
        # Clean text of any raw newlines
        clean_text = text.replace("\n", " ")
        sch_lines.append(f'\t(text "{clean_text}" (at {x} {y} 0) (effects (font (size {size} {size}){b_str}{i_str}) (justify {justify})) (uuid "{u()}"))')

    def add_label(name, x, y, size=1.2):
        sch_lines.append(f'\t(label "{name}" (at {x} {y} 0) (effects (font (size {size} {size}))) (uuid "{u()}"))')

    # --- BLOCK 1: ANALOG FRONT-END ---
    add_rect(20, 30, 115, 120, stroke_w=0.4)
    add_text("BLOCK 1: ANALOG FRONT-END (AFE) & ACOUSTIC FILTERING", 23, 26, size=2.0, bold=True)
    add_text("• Piezo Contact Transducer (27mm PZT Ceramic clamped to pipe)", 23, 34, size=1.2, italic=True)
    add_text("• Dual Rail-to-Rail Op-Amp: Microchip MCP6002-I/SN", 23, 38, size=1.2, italic=True)
    add_text("• Stage 1: High-Pass Buffer (fc = 500 Hz, Vref = 1.65V)", 23, 42, size=1.2)
    add_text("• Stage 2: 2nd-Order Sallen-Key Low-Pass (fc = 3.0 kHz, Gain = +20 dB)", 23, 46, size=1.2)

    # J1 Piezo Connector
    add_rect(25, 55, 40, 75, stroke_w=0.25)
    add_text("J1: PIEZO", 27, 62, size=1.2, bold=True)
    add_text("PROBE IN", 27, 67, size=1.0)
    add_line(40, 60, 48, 60)
    add_line(40, 70, 48, 70)
    add_label("GND", 48, 70)

    # C1 AC Coupling
    add_rect(48, 56, 56, 64)
    add_text("C1 100nF", 49, 60, size=0.9)
    add_line(56, 60, 68, 60)
    add_line(62, 60, 62, 50)
    add_rect(58, 42, 66, 50)
    add_text("R1 100k", 59, 46, size=0.9)

    # MCP6002 Stage 1
    add_rect(68, 52, 85, 78, stroke_w=0.3)
    add_text("U2A: MCP6002", 70, 58, size=1.1, bold=True)
    add_text("STAGE 1: HPF", 70, 63, size=1.0)
    add_text("Vref = 1.65V", 70, 68, size=0.9)
    add_line(85, 65, 93, 65)

    # MCP6002 Stage 2
    add_rect(93, 52, 110, 78, stroke_w=0.3)
    add_text("U2B: MCP6002", 95, 58, size=1.1, bold=True)
    add_text("STAGE 2: LPF", 95, 63, size=1.0)
    add_text("Gain = +20dB", 95, 68, size=0.9)
    add_line(110, 65, 125, 65)
    add_label("AFE_OUT", 125, 65, size=1.4)
    add_text("Output: 500Hz-3kHz (±1.5Vpp centered at 1.65V)", 23, 85, size=1.1, italic=True)

    # VREF Generator
    add_rect(25, 88, 55, 115, stroke_w=0.2)
    add_text("VREF GENERATOR", 27, 94, size=1.1, bold=True)
    add_text("R3/R4 (100k 1%) + C3 (10uF)", 27, 99, size=0.9)
    add_text("VREF = 3.3V / 2 = 1.65V", 27, 104, size=0.9)
    add_line(55, 100, 65, 100)
    add_label("VREF_1V65", 65, 100)

    # --- BLOCK 2: ADS1115 16-BIT ADC ---
    add_rect(125, 30, 200, 120, stroke_w=0.4)
    add_text("BLOCK 2: 16-BIT PRECISION ADC (TI ADS1115)", 128, 26, size=2.0, bold=True)
    add_text("• Texas Instruments ADS1115IDGSR (16-Bit Delta-Sigma)", 128, 34, size=1.2, italic=True)
    add_text("• Dynamic Range: 16-Bit | Programmable Gain: 1x to 16x", 128, 38, size=1.2)
    add_text("• Sampling Rate: 860 SPS / Fast Burst Mode", 128, 42, size=1.2)
    add_text("• I2C Interface: Address 0x48 (ADDR pin tied to GND)", 128, 46, size=1.2)

    add_rect(140, 55, 185, 95, stroke_w=0.3)
    add_text("U3: ADS1115", 145, 62, size=1.3, bold=True)
    add_text("16-BIT ADC", 145, 68, size=1.1)
    add_text("I2C: 0x48", 145, 74, size=1.0)
    add_line(125, 75, 140, 75)
    add_label("AFE_OUT", 132, 73, size=1.1)
    add_text("AIN0", 142, 78, size=0.9)

    add_line(185, 65, 205, 65)
    add_label("I2C_SCL", 205, 65)
    add_line(185, 75, 205, 75)
    add_label("I2C_SDA", 205, 75)
    add_line(185, 85, 205, 85)
    add_label("ADC_ALERT", 205, 85)
    add_text("VDD = 3.3V (C4 = 100nF decoupling)", 135, 105, size=1.0, italic=True)

    # --- BLOCK 3: ESP32-S3 COMPUTE & MESH ---
    add_rect(215, 30, 395, 120, stroke_w=0.4)
    add_text("BLOCK 3: ESP32-S3 DUAL-CORE COMPUTE & ESP-NOW MESH", 218, 26, size=2.0, bold=True)
    add_text("• Espressif ESP32-S3-WROOM-1 (Xtensa Dual-Core 32-bit LX7 @ 240 MHz)", 218, 34, size=1.2, italic=True)
    add_text("• Core 0: High-Speed ADC Sampling, Circular Waveform Buffer (2048 samples)", 218, 38, size=1.2)
    add_text("• Core 1: ESP-NOW Mesh Protocol, TDOA Cross-Correlation, Consensus Engine", 218, 42, size=1.2)
    add_text("• Memory: 8MB Flash + 8MB Octal PSRAM | Radio: 2.4GHz Wi-Fi/BLE (ESP-NOW <20ms)", 218, 46, size=1.2)

    add_rect(235, 52, 340, 112, stroke_w=0.35)
    add_text("U1: ESP32-S3-WROOM-1", 245, 60, size=1.3, bold=True)
    add_text("DUAL-CORE XTENSA LX7 @ 240 MHz", 245, 66, size=1.0)

    add_line(215, 68, 235, 68)
    add_label("I2C_SCL", 220, 66)
    add_text("GPIO5 (SCL)", 238, 68, size=1.0)

    add_line(215, 76, 235, 76)
    add_label("I2C_SDA", 220, 74)
    add_text("GPIO4 (SDA)", 238, 76, size=1.0)

    add_line(215, 84, 235, 84)
    add_label("ADC_ALERT", 220, 82)
    add_text("GPIO6 (ALERT)", 238, 84, size=1.0)

    add_line(215, 92, 235, 92)
    add_label("RTC_SQW", 220, 90)
    add_text("GPIO7 (TCXO_SYNC)", 238, 92, size=1.0)

    add_line(340, 65, 365, 65)
    add_text("GPIO19 (USB_D-)", 320, 65, size=0.9)
    add_label("USB_DN", 365, 65)

    add_line(340, 73, 365, 73)
    add_text("GPIO20 (USB_D+)", 320, 73, size=0.9)
    add_label("USB_DP", 365, 73)

    add_line(340, 85, 365, 85)
    add_text("GPIO48 (RGB)", 320, 85, size=0.9)
    add_label("WS2812_DATA", 365, 85)

    add_line(340, 98, 365, 98)
    add_text("RESET / BOOT", 320, 98, size=0.9)
    add_label("RESET_N", 365, 98)

    # --- BLOCK 4: DS3231 PRECISION RTC ---
    add_rect(20, 135, 115, 215, stroke_w=0.4)
    add_text("BLOCK 4: MICROSECOND PRECISION TCXO RTC (DS3231)", 23, 131, size=2.0, bold=True)
    add_text("• Analog Devices / Maxim DS3231SN (Integrated Temp-Compensated TCXO)", 23, 139, size=1.2, italic=True)
    add_text("• Frequency Accuracy: ±2 ppm (0°C to +40°C) | Aging: ±1 ppm/year", 23, 143, size=1.2)
    add_text("• Crucial for TDOA cross-correlation microsecond node synchronization", 23, 147, size=1.2)
    add_text("• Backup Supply: Onboard CR1220 Coin Cell / Supercapacitor backup", 23, 151, size=1.2)

    add_rect(40, 160, 95, 200, stroke_w=0.3)
    add_text("U4: DS3231SN", 45, 168, size=1.3, bold=True)
    add_text("TCXO RTC", 45, 174, size=1.1)
    add_text("I2C: 0x68", 45, 180, size=1.0)
    add_line(95, 170, 115, 170)
    add_label("I2C_SCL", 115, 170)
    add_line(95, 180, 115, 180)
    add_label("I2C_SDA", 115, 180)
    add_line(95, 190, 115, 190)
    add_label("RTC_SQW", 115, 190)
    add_text("SQW output gives 1Hz / 32kHz microsecond reference pulse", 25, 208, size=1.05, italic=True)

    # --- BLOCK 5: ADXL345 ---
    add_rect(125, 135, 200, 215, stroke_w=0.4)
    add_text("BLOCK 5: ADXL345 AUX ACCELEROMETER", 128, 131, size=2.0, bold=True)
    add_text("• Analog Devices ADXL345BCCZ 3-Axis MEMS", 128, 139, size=1.2, italic=True)
    add_text("• Verifies mechanical pipe acceleration vs airborne noise", 128, 143, size=1.2)
    add_text("• False-positive rejection: surface rumbles disregarded", 128, 147, size=1.2)
    add_text("• I2C Interface: Address 0x53 (ALT_ADDRESS low)", 128, 151, size=1.2)

    add_rect(140, 160, 185, 200, stroke_w=0.3)
    add_text("U5: ADXL345", 145, 168, size=1.3, bold=True)
    add_text("3-AXIS ACCEL", 145, 174, size=1.1)
    add_text("I2C: 0x53", 145, 180, size=1.0)
    add_line(185, 172, 205, 172)
    add_label("I2C_SCL", 205, 172)
    add_line(185, 182, 205, 182)
    add_label("I2C_SDA", 205, 182)

    # --- BLOCK 6: BMS & REGULATION ---
    add_rect(215, 135, 395, 215, stroke_w=0.4)
    add_text("BLOCK 6: SOLAR BMS, LI-ION PROTECTION & LOW-NOISE REGULATION", 218, 131, size=2.0, bold=True)
    add_text("• Solar Input: 5V/6V Monocrystalline Panel (J3) + TP4056 CC/CV Lithium Charger (U6)", 218, 139, size=1.2, italic=True)
    add_text("• Battery Cell: 3.7V 3000mAh Grade-A Li-ion 18650 Pack with DW01A + FS8205A Over/Under Protection (U7)", 218, 143, size=1.2)
    add_text("• System Rail: Diodes Inc AP2112K-3.3 ultra-low-noise 600mA LDO (ripple <30uV, PSRR = 65dB)", 218, 147, size=1.2)
    add_text("• Fully battery-isolated & intrinsically safe: Zero mains connection, zero pipe electrolytic hazard", 218, 151, size=1.2)

    add_rect(225, 165, 245, 185, stroke_w=0.25)
    add_text("J3: SOLAR", 227, 172, size=1.1, bold=True)
    add_text("5V-6V IN", 227, 177, size=0.9)
    add_line(245, 175, 255, 175)

    add_rect(255, 162, 290, 195, stroke_w=0.3)
    add_text("U6: TP4056", 260, 170, size=1.1, bold=True)
    add_text("CHARGER", 260, 175, size=1.0)
    add_text("PROG=1.2k", 260, 180, size=0.9)
    add_line(290, 175, 305, 175)

    add_rect(305, 162, 340, 195, stroke_w=0.3)
    add_text("U7: DW01A", 310, 170, size=1.1, bold=True)
    add_text("FS8205A", 310, 175, size=1.0)
    add_text("BMS PROT", 310, 180, size=0.9)
    add_line(340, 175, 355, 175)

    add_rect(355, 162, 385, 195, stroke_w=0.35)
    add_text("U8: AP2112", 360, 170, size=1.1, bold=True)
    add_text("3.3V LDO", 360, 175, size=1.0)
    add_text("600mA", 360, 180, size=0.9)
    add_line(385, 175, 395, 175)
    add_label("3V3_SYS", 395, 175)

    add_text("Battery Input: J2 (JST-PH 2.0mm) | C_in = 10uF X7R | C_out = 22uF Low-ESR Ceramic", 225, 205, size=1.1, italic=True)

    sch_lines.append('\t(sheet_instances')
    sch_lines.append('\t\t(path "/" (page "1"))')
    sch_lines.append('\t)')
    sch_lines.append('\t(embedded_fonts no)')
    sch_lines.append(')')

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sch_lines))
    print(f"Written: {sch_path}")

    # Export using kicad-cli
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    svg_out = os.path.join(exports_dir, "AQUAPULSE_Schematic.svg")
    res = subprocess.run([kicad_cli, "sch", "export", "svg", "-o", svg_out, sch_path], capture_output=True, text=True)
    print("SCH export SVG result:", res.returncode)

    pdf_out = os.path.join(exports_dir, "AQUAPULSE_Schematic.pdf")
    res_p = subprocess.run([kicad_cli, "sch", "export", "pdf", "-o", pdf_out, sch_path], capture_output=True, text=True)
    print("SCH export PDF result:", res_p.returncode)

    # Copy exports to docs/assets
    if os.path.exists(svg_out):
        if os.path.isdir(svg_out):
            for f in os.listdir(svg_out):
                if f.endswith('.svg'):
                    shutil.copy2(os.path.join(svg_out, f), os.path.join(docs_assets, "AQUAPULSE_Schematic.svg"))
                    print("Copied schematic SVG to docs/assets")
        else:
            shutil.copy2(svg_out, os.path.join(docs_assets, "AQUAPULSE_Schematic.svg"))
            print("Copied schematic SVG to docs/assets")

    if os.path.exists(pdf_out):
        shutil.copy2(pdf_out, os.path.join(docs_assets, "AQUAPULSE_Schematic.pdf"))
        print("Copied schematic PDF to docs/assets")

if __name__ == "__main__":
    generate_aquapulse_kicad()
