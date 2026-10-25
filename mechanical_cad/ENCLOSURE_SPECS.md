# AQUAPULSE Enclosure & Mechanical CAD Specifications

**System:** Non-Invasive Clamp-On Acoustic Triangulation Node  
**Track Alignment:** Maker Bhavan Foundation — Vishwakarma Awards 2026–27  
**Host Institute:** IIT Hyderabad | **Theme:** Sustainable Cities  
**CAD Format:** Wavefront OBJ, Material MTL, Standard STL, Blender Python Rig (`.py`)

---

## 1. Mechanical Assembly Architecture

The AQUAPULSE sensor node is engineered for **non-invasive, clamp-on deployment** across municipal water distribution pipes ranging from **100 mm to 300 mm outer diameter** (Ductile Iron, Cast Iron, PVC, HDPE).

```
                      +-----------------------------+
                      |   Monocrystalline Solar     |
                      |   Harvester (60 x 60 mm)    |
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      |  Enclosure Top Lid (ABS/PC) |
                      |  with Status LED Diffuser   |
                      +--------------+--------------+
                                     |
                         [ Silicone O-Ring Gasket ]  <-- IP67 Submersion Seal
                                     |
                      +--------------v--------------+
                      |  Main Electronics Enclosure |
                      |  (ESP32-S3 + AFE + ADS1115) |
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      |  Magnetic Saddle Mount      |
                      |  4x N52 Neodymium Magnets   |
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      | Spring-Loaded Acoustic Probe|
                      | 27mm PZT Ceramic Contact    |
                      +--------------+--------------+
                                     |
                     =================================
                       WATER PIPELINE (100 - 300 mm)
                     =================================
```

---

## 2. Ingress Protection & Environmental Engineering (IP67)

| Parameter | Specification | Engineering Mechanism |
| :--- | :--- | :--- |
| **Ingress Protection Rating** | **IP67 Certified** | Continuous tongue-and-groove silicone gasket channel with 15% compression under M3 stainless torx fasteners. |
| **Operating Temperature** | **-10°C to +65°C** | High heat deflection temperature (HDT @ 0.45 MPa: 95°C) using UV-stabilized Polycarbonate/ABS blend. |
| **Moisture & Condensation** | **Breather Membrane** | Gore-Tex ePTFE pressure equalization vent prevents internal vacuum suction during nocturnal temperature drops. |
| **Corrosion Resistance** | **ISO 9227 Salt Spray** | 316 Stainless steel screws and nickel-plated neodymium magnets prevent galvanic pipe reactions. |
| **Vibration Tolerance** | **IEC 60068-2-6** | Internal PCB cushioned on elastomeric dampening standoffs; resonant frequency tuned above 4.5 kHz. |

---

## 3. Acoustic Coupling & Spring-Loaded Probe Dynamics

Direct acoustic transmission from the pipe wall to the piezo transducer is critical for sub-meter TDOA cross-correlation accuracy:
1. **PZT Disc Integration:** A 27 mm diameter piezoelectric ceramic disc (Murata PZT) is encased in a CNC-machined brass contact cup.
2. **Spring Pre-load:** A calibrated helical spring (15 N pre-load force) pushes the probe downwards against the outer pipe surface through the center aperture of the saddle bracket.
3. **Acoustic Impedance Matching:** A 1.5 mm thick closed-cell acoustic silicone pad with acoustic coupling grease (silicone vacuum grease) eliminates air gaps between the rough cast-iron pipe surface and the transducer.

---

## 4. CAD & Blender File Directory

| File | Type | Description |
| :--- | :---: | :--- |
| [`aquapulse_full_assembly.obj`](./aquapulse_full_assembly.obj) | 3D Mesh | Full multi-part textured assembly for CAD viewers & Blender. |
| [`aquapulse_full_assembly.mtl`](./aquapulse_full_assembly.mtl) | Materials | PBR material definitions (die-cast ABS, brass, solar glass, neodymium). |
| [`enclosure_base_ip67.stl`](./enclosure_base_ip67.stl) | STL | 3D-printable base housing with cable gland ports and PCB mounting bosses. |
| [`enclosure_top_lid.stl`](./enclosure_top_lid.stl) | STL | 3D-printable top lid with 60x60mm solar panel recess and light pipe. |
| [`magnetic_pipe_mount_saddle.stl`](./magnetic_pipe_mount_saddle.stl) | STL | Pipe-contour bracket with 4x 20mm magnet pockets and clamp strap slots. |
| [`acoustic_coupling_probe.stl`](./acoustic_coupling_probe.stl) | STL | Spring-loaded brass acoustic probe for 27mm piezo contact element. |
| [`blender_render_rig.py`](./blender_render_rig.py) | Python | Automated Blender studio script for 3-point lighting & exploded view animation. |
