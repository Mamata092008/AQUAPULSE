# AQUAPULSE Node — Hardware Bill of Materials (BOM)

**Project:** AQUAPULSE Non-Invasive Acoustic Sensor Node  
**Team:** TECHTONICS | **Competition:** Vishwakarma Awards 2026–27 (IIT Hyderabad)  
**Hardware Revision:** v1.2-PRO  

| Item | Designator | Part Number | Manufacturer | Description | Package | Qty | Cost (INR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | `U1` | **ESP32-S3-WROOM-1-N8R8** | Espressif | Dual-Core Xtensa LX7 MCU, 240MHz, 8MB Flash, 8MB PSRAM, Wi-Fi 4 / BLE 5 | `SMD Module` | 1 | ₹380.00 |
| 2 | `U2` | **MCP6002-I/SN** | Microchip | Dual Rail-to-Rail Ultra-Low-Noise Operational Amplifier (1 MHz GBWP) | `SOIC-8` | 1 | ₹65.00 |
| 3 | `U3` | **ADS1115IDGSR** | Texas Instruments | 16-Bit Ultra-Compact Delta-Sigma ADC with Internal Reference and PGA | `MSOP-10` | 1 | ₹240.00 |
| 4 | `U4` | **DS3231SN#** | Analog Devices / Maxim | Extremely Accurate I2C Integrated TCXO/RTC (±2ppm from 0°C to +40°C) | `SOIC-16W` | 1 | ₹180.00 |
| 5 | `U5` | **ADXL345BCCZ** | Analog Devices | 3-Axis Digital MEMS Accelerometer for Structural Vibration Cross-Check | `LGA-14` | 1 | ₹120.00 |
| 6 | `U6` | **TP4056 + DW01A** | NanJing Top Power | 1A Standalone Li-ion Constant Current/Voltage Charger + Battery Protection | `SOP-8` | 1 | ₹35.00 |
| 7 | `U7` | **AP2112K-3.3TRG1** | Diodes Incorporated | 600mA Ultra-Low-Noise CMOS LDO Linear Regulator (3.3V Output) | `SOT-23-5` | 1 | ₹25.00 |
| 8 | `S1` | **PZT-27B-1.5A** | Murata / Generic | High-Sensitivity 27mm Piezoelectric Ceramic Contact Acoustic Transducer | `Clamp Disc` | 1 | ₹120.00 |
| 9 | `BAT1` | **INR18650-30Q** | Samsung / EVE | 3.7V 3000mAh Grade-A Li-ion Cell with Integrated Protection Lead | `18650 Pack` | 1 | ₹220.00 |
| 10 | `SOL1` | **SP-5V-1W** | Generic Monocrystalline | 5V 200mA (1W) Weather-Sealed Monocrystalline Solar Harvesting Panel | `60x60mm Panel` | 1 | ₹150.00 |
| 11 | `ENC1` | **IP67-ABS-1007** | Gainta / Generic | IP67 Waterproof Die-Cast ABS/Polycarbonate Enclosure with Silicone Gasket | `Enclosure` | 1 | ₹280.00 |
| 12 | `MNT1` | **MAG-N52-SADDLE** | Custom 3D + Neodymium | Magnetic Pipe Contour Saddle Bracket with 4x N52 Neodymium Pot Magnets | `Assembly` | 1 | ₹180.00 |
| 13 | `PASSIVES` | **0805 SMD Passives** | Yageo / Murata | 1% Thin-Film Resistors, C0G/X7R Capacitors, Ferrite Beads, Inductor | `0805 SMD` | 24 | ₹55.00 |

---
### Economic Summary
- **Total Single-Node Prototype BOM Cost:** **₹2,050.00**
- **Projected Mass Production BOM (1,000+ Units, Bulk Automated SMT):** **₹900.00**
- **Comparison with Commercial Manual Acoustic Survey:** A single 1-week contracted survey for a 5 km pipeline costs ₹1,00,000 to ₹1,50,000. For the same cost, **over 50 AQUAPULSE nodes can be permanently installed** to provide 24/7 autonomous monitoring for years.
