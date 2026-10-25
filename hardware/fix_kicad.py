import os
import subprocess
import uuid
import shutil

def u():
    return str(uuid.uuid4())

kicad_dir = r"f:\HACKATHONS\vishwakarma\AQUAPULSE\hardware\kicad"
exports_dir = os.path.join(kicad_dir, "exports")
docs_assets = r"f:\HACKATHONS\vishwakarma\AQUAPULSE\docs\assets"

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
    '\t\t(rev "v1.2")',
    '\t\t(company "Team TECHTONICS | Vishwakarma Awards 2026-27 (Host: IIT Hyderabad)")',
    '\t)',
    '\t(lib_symbols)'
]

def add_rect(x1, y1, x2, y2, stroke_w=0.3):
    sch_lines.append(f'\t(polyline (pts (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2}) (xy {x1} {y1}))')
    sch_lines.append(f'\t\t(stroke (width {stroke_w}) (type default))')
    sch_lines.append(f'\t\t(uuid "{u()}")')
    sch_lines.append('\t)')

def add_line(x1, y1, x2, y2, stroke_w=0.25):
    sch_lines.append(f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2}))')
    sch_lines.append(f'\t\t(stroke (width {stroke_w}) (type default))')
    sch_lines.append(f'\t\t(uuid "{u()}")')
    sch_lines.append('\t)')

def add_text(text, x, y, size=1.5, bold=False, italic=False, justify="left"):
    b_str = " (bold yes)" if bold else ""
    i_str = " (italic yes)" if italic else ""
    sch_lines.append(f'\t(text "{text}" (at {x} {y} 0)')
    sch_lines.append(f'\t\t(effects (font (size {size} {size}){b_str}{i_str}) (justify {justify}))')
    sch_lines.append(f'\t\t(uuid "{u()}")')
    sch_lines.append('\t)')

def add_label(name, x, y, size=1.2, justify="left"):
    sch_lines.append(f'\t(label "{name}" (at {x} {y} 0)')
    sch_lines.append(f'\t\t(effects (font (size {size} {size}) (bold yes)) (justify {justify}))')
    sch_lines.append(f'\t\t(uuid "{u()}")')
    sch_lines.append('\t)')

# Block 1: Analog Front-End (AFE)
add_rect(20, 30, 115, 120, stroke_w=0.4)
add_text("BLOCK 1: ANALOG FRONT-END (AFE) & ACOUSTIC FILTERING", 23, 26, size=2.0, bold=True)
add_text("• Piezo Contact Transducer (27mm PZT Ceramic clamped to pipe)", 23, 34, size=1.2, italic=True)
add_text("• Dual Rail-to-Rail Op-Amp: Microchip MCP6002-I/SN", 23, 38, size=1.2, italic=True)
add_text("• Stage 1: High-Pass Buffer (fc = 500 Hz, Vref = 1.65V)", 23, 42, size=1.2)
add_text("• Stage 2: 2nd-Order Sallen-Key Low-Pass (fc = 3.0 kHz, Gain = +20 dB)", 23, 46, size=1.2)

# J1 Piezo Connector
add_rect(25, 55, 38, 75, stroke_w=0.25)
add_text("J1\\nPIEZO\\nPROBE", 31.5, 63, size=1.3, bold=True, justify="center")
add_line(38, 60, 48, 60)
add_line(38, 70, 48, 70)
add_label("GND", 48, 70)

# C1 AC Coupling
add_rect(48, 56, 56, 64)
add_text("C1\\n100nF", 52, 60, size=1.0, justify="center")
add_line(56, 60, 68, 60)
add_line(62, 60, 62, 50)
add_rect(58, 42, 66, 50)
add_text("R1 100k\\n(to VREF)", 62, 46, size=0.9, justify="center")

# MCP6002 Stage 1
add_rect(68, 52, 85, 78, stroke_w=0.3)
add_text("U2A: MCP6002\\nSTAGE 1\\nHPF & BUFFER", 76.5, 63, size=1.2, bold=True, justify="center")
add_line(85, 65, 93, 65)

# MCP6002 Stage 2
add_rect(93, 52, 110, 78, stroke_w=0.3)
add_text("U2B: MCP6002\\nSTAGE 2\\nSALLEN-KEY", 101.5, 63, size=1.2, bold=True, justify="center")
add_line(110, 65, 125, 65)
add_label("AFE_OUT", 125, 65, size=1.4)
add_text("Signal: 500Hz-3kHz, ±1.5Vpp\\nCentered at 1.65V VREF", 68, 85, size=1.1, italic=True)

# VREF Generator
add_rect(25, 88, 55, 115, stroke_w=0.2)
add_text("VREF GENERATOR\\nR3/R4 (100k 1%) + C3 (10uF)\\nVREF = 3.3V / 2 = 1.65V", 40, 100, size=1.1, justify="center")
add_line(55, 100, 65, 100)
add_label("VREF_1V65", 65, 100)

# Block 2: ADS1115
add_rect(125, 30, 200, 120, stroke_w=0.4)
add_text("BLOCK 2: 16-BIT PRECISION ADC (TI ADS1115)", 128, 26, size=2.0, bold=True)
add_text("• Texas Instruments ADS1115IDGSR (16-Bit Delta-Sigma)", 128, 34, size=1.2, italic=True)
add_text("• Dynamic Range: 16-Bit | Programmable Gain: 1x to 16x", 128, 38, size=1.2)
add_text("• Sampling Rate: Configured up to 860 SPS / Fast Burst Mode", 128, 42, size=1.2)
add_text("• I2C Interface: Address 0x48 (ADDR pin tied to GND)", 128, 46, size=1.2)

add_rect(140, 55, 185, 95, stroke_w=0.3)
add_text("U3: ADS1115\\n16-BIT ADC\\n(I2C: 0x48)", 162.5, 65, size=1.4, bold=True, justify="center")
add_line(125, 75, 140, 75)
add_label("AFE_OUT", 132, 73, size=1.1)
add_text("AIN0 (Pin 3)", 143, 75, size=1.0)
add_line(185, 65, 205, 65)
add_label("I2C_SCL", 205, 65)
add_line(185, 75, 205, 75)
add_label("I2C_SDA", 205, 75)
add_line(185, 85, 205, 85)
add_label("ADC_ALERT", 205, 85)
add_text("VDD = 3.3V (C4 = 100nF decoupling)\\nADDR = GND | AIN1-3 = Filtered", 135, 108, size=1.1, italic=True)

# Block 3: ESP32-S3
add_rect(215, 30, 395, 120, stroke_w=0.4)
add_text("BLOCK 3: ESP32-S3 DUAL-CORE COMPUTE & ESP-NOW MESH", 218, 26, size=2.0, bold=True)
add_text("• Espressif ESP32-S3-WROOM-1 (Xtensa Dual-Core 32-bit LX7 @ 240 MHz)", 218, 34, size=1.2, italic=True)
add_text("• Core 0: High-Speed ADC Sampling, Circular Waveform Buffer (2048 samples), RMS Noise Baseline", 218, 38, size=1.2)
add_text("• Core 1: ESP-NOW Mesh Protocol, TDOA Cross-Correlation Engine, Consensus Validation", 218, 42, size=1.2)
add_text("• Memory: 8MB Flash + 8MB Octal PSRAM | Radio: 2.4GHz Wi-Fi/BLE (ESP-NOW broadcast <20ms)", 218, 46, size=1.2)

add_rect(235, 52, 340, 112, stroke_w=0.35)
add_text("U1: ESP32-S3-WROOM-1\\nDUAL-CORE XTENSA LX7 @ 240 MHz", 287.5, 60, size=1.4, bold=True, justify="center")

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
add_text("GPIO19 (USB_D-)", 325, 65, size=1.0, justify="right")
add_label("USB_DN", 365, 65)

add_line(340, 73, 365, 73)
add_text("GPIO20 (USB_D+)", 325, 73, size=1.0, justify="right")
add_label("USB_DP", 365, 73)

add_line(340, 85, 365, 85)
add_text("GPIO48 (NEOPIXEL)", 325, 85, size=1.0, justify="right")
add_label("WS2812_DATA", 365, 85)

add_line(340, 98, 365, 98)
add_text("EN / BOOT / RESET", 325, 98, size=1.0, justify="right")
add_label("RESET_N", 365, 98)

# Block 4: DS3231 RTC
add_rect(20, 135, 115, 215, stroke_w=0.4)
add_text("BLOCK 4: MICROSECOND PRECISION TCXO RTC (DS3231)", 23, 131, size=2.0, bold=True)
add_text("• Analog Devices / Maxim DS3231SN (Integrated Temp-Compensated TCXO)", 23, 139, size=1.2, italic=True)
add_text("• Frequency Accuracy: ±2 ppm (0°C to +40°C) | Aging: ±1 ppm/year", 23, 143, size=1.2)
add_text("• Crucial for TDOA cross-correlation microsecond node synchronization", 23, 147, size=1.2)
add_text("• Backup Supply: Onboard CR1220 Coin Cell / Supercapacitor backup", 23, 151, size=1.2)

add_rect(40, 160, 95, 200, stroke_w=0.3)
add_text("U4: DS3231SN\\nTCXO RTC\\n(I2C: 0x68)", 67.5, 172, size=1.3, bold=True, justify="center")
add_line(95, 170, 115, 170)
add_label("I2C_SCL", 115, 170)
add_line(95, 180, 115, 180)
add_label("I2C_SDA", 115, 180)
add_line(95, 190, 115, 190)
add_label("RTC_SQW", 115, 190)
add_text("SQW output gives 1Hz / 32kHz microsecond reference pulse", 25, 208, size=1.05, italic=True)

# Block 5: ADXL345
add_rect(125, 135, 200, 215, stroke_w=0.4)
add_text("BLOCK 5: ADXL345 AUX ACCELEROMETER", 128, 131, size=2.0, bold=True)
add_text("• Analog Devices ADXL345BCCZ 3-Axis MEMS", 128, 139, size=1.2, italic=True)
add_text("• Verifies mechanical pipe acceleration vs airborne noise", 128, 143, size=1.2)
add_text("• False-positive rejection: surface rumbles disregarded", 128, 147, size=1.2)
add_text("• I2C Interface: Address 0x53 (ALT_ADDRESS low)", 128, 151, size=1.2)

add_rect(140, 160, 185, 200, stroke_w=0.3)
add_text("U5: ADXL345\\n3-AXIS ACCEL\\n(I2C: 0x53)", 162.5, 172, size=1.3, bold=True, justify="center")
add_line(185, 172, 205, 172)
add_label("I2C_SCL", 205, 172)
add_line(185, 182, 205, 182)
add_label("I2C_SDA", 205, 182)

# Block 6: BMS & Power
add_rect(215, 135, 395, 215, stroke_w=0.4)
add_text("BLOCK 6: SOLAR BMS, LI-ION PROTECTION & LOW-NOISE REGULATION", 218, 131, size=2.0, bold=True)
add_text("• Solar Input: 5V/6V Monocrystalline Panel (J3) + TP4056 CC/CV Lithium Charger (U6)", 218, 139, size=1.2, italic=True)
add_text("• Battery Cell: 3.7V 3000mAh Grade-A Li-ion 18650 Pack with DW01A + FS8205A Over/Under Protection (U7)", 218, 143, size=1.2)
add_text("• System Rail: Diodes Inc AP2112K-3.3 ultra-low-noise 600mA LDO (ripple <30uV, PSRR = 65dB)", 218, 147, size=1.2)
add_text("• Fully battery-isolated & intrinsically safe: Zero mains connection, zero pipe electrolytic hazard", 218, 151, size=1.2)

add_rect(225, 165, 245, 185, stroke_w=0.25)
add_text("J3\\nSOLAR\\n5V-6V", 235, 172, size=1.1, bold=True, justify="center")
add_line(245, 175, 255, 175)

add_rect(255, 162, 290, 195, stroke_w=0.3)
add_text("U6: TP4056\\nLI-ION CHARGER\\nPROG = 1.2k (1A)", 272.5, 175, size=1.1, bold=True, justify="center")
add_line(290, 175, 305, 175)

add_rect(305, 162, 340, 195, stroke_w=0.3)
add_text("U7: DW01A +\\nFS8205A MOSFET\\nBMS PROTECTION", 322.5, 175, size=1.1, bold=True, justify="center")
add_line(340, 175, 355, 175)

add_rect(355, 162, 385, 195, stroke_w=0.35)
add_text("U8: AP2112K\\n3.3V 600mA\\nLOW NOISE LDO", 370, 175, size=1.1, bold=True, justify="center")
add_line(385, 175, 395, 175)
add_label("3V3_SYS", 395, 175, size=1.3)

add_text("Battery Input: J2 (JST-PH 2.0mm) | C_in = 10uF X7R | C_out = 22uF Low-ESR Ceramic", 225, 205, size=1.1, italic=True)

sch_lines.append('\t(sheet_instances')
sch_lines.append('\t\t(path "/" (page "1"))')
sch_lines.append('\t)')
sch_lines.append('\t(embedded_fonts no)')
sch_lines.append(')')

with open(sch_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sch_lines))
print(f"Written: {sch_path}")

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
svg_out = os.path.join(exports_dir, "AQUAPULSE_Schematic.svg")
res = subprocess.run([kicad_cli, "sch", "export", "svg", "-o", svg_out, sch_path], capture_output=True, text=True)
print("SCH export SVG result:", res.returncode, res.stdout, res.stderr)

pdf_out = os.path.join(exports_dir, "AQUAPULSE_Schematic.pdf")
res_p = subprocess.run([kicad_cli, "sch", "export", "pdf", "-o", pdf_out, sch_path], capture_output=True, text=True)
print("SCH export PDF result:", res_p.returncode, res_p.stdout, res_p.stderr)

# Copy to docs/assets
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
