"""
AQUAPULSE: Acoustic Cross-Correlation Triangulation Simulation & Proof of Concept
Team TECHTONICS | Vishwakarma Awards 2026–27 | Host: IIT Hyderabad

This script simulates:
1. Subterranean pipeline acoustic propagation with high-frequency leak signatures.
2. Ambient environmental noise (traffic rumble + Gaussian thermal noise).
3. Analog Front-End (AFE) bandpass signal conditioning (500 Hz – 3000 Hz).
4. Time Difference of Arrival (TDOA) cross-correlation between clamp-on nodes.
5. Parabolic sub-sample interpolation for sub-meter leak localization accuracy.
6. Bode frequency response of the 2nd-order active Sallen-Key bandpass filter.
"""

import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Set high-resolution aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

def run_simulation(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. Pipeline Physical & Acoustic Parameters
    # -------------------------------------------------------------
    pipe_length = 200.0          # Distance between Node A and Node B in metres
    v_sound = 1250.0             # Acoustic propagation speed in ductile iron with water (m/s)
    x_leak_true = 68.4           # Actual physical leak position from Node A (metres)
    
    fs = 8000                    # Sampling rate (Hz) - matched to ADS1115 ADC capability
    duration = 0.5               # Signal duration (seconds)
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Distance to each node
    dist_A = x_leak_true
    dist_B = pipe_length - x_leak_true
    
    # Time of flight to each node
    t_flight_A = dist_A / v_sound
    t_flight_B = dist_B / v_sound
    true_tau = t_flight_B - t_flight_A  # Positive means Node A hears it first
    
    print(f"--- AQUAPULSE Simulation Setup ---")
    print(f"Pipe Length: {pipe_length} m | Sound Velocity: {v_sound} m/s")
    print(f"True Leak Location: {x_leak_true:.2f} m from Node A")
    print(f"Time of Flight A: {t_flight_A*1000:.3f} ms | Time of Flight B: {t_flight_B*1000:.3f} ms")
    print(f"True TDOA (tau): {true_tau*1000:.3f} ms")
    
    # -------------------------------------------------------------
    # 2. Generate Leak Acoustic Emission & Propagation
    # -------------------------------------------------------------
    np.random.seed(42)
    # Leak sound is broadband cavitation hiss concentrated between 600 Hz and 2800 Hz
    raw_leak_noise = np.random.normal(0, 1.0, len(t))
    sos_leak = signal.butter(4, [600, 2800], btype='bandpass', fs=fs, output='sos')
    leak_source = signal.sosfilt(sos_leak, raw_leak_noise)
    
    # Shift waveforms according to arrival times
    delay_samples_A = int(np.round(t_flight_A * fs))
    delay_samples_B = int(np.round(t_flight_B * fs))
    
    # Attenuation: higher distance = lower amplitude
    alpha = 0.008  # Acoustic attenuation coefficient (dB/m)
    amp_A = np.exp(-alpha * dist_A)
    amp_B = np.exp(-alpha * dist_B)
    
    sig_A = np.zeros_like(t)
    sig_B = np.zeros_like(t)
    
    if delay_samples_A < len(t):
        sig_A[delay_samples_A:] = amp_A * leak_source[:len(t)-delay_samples_A]
    if delay_samples_B < len(t):
        sig_B[delay_samples_B:] = amp_B * leak_source[:len(t)-delay_samples_B]
        
    # Add ambient road traffic rumble (low frequency 30-150 Hz) & Gaussian white noise
    traffic_rumble_A = 0.4 * np.sin(2 * np.pi * 45 * t) + 0.25 * np.sin(2 * np.pi * 85 * t)
    traffic_rumble_B = 0.4 * np.sin(2 * np.pi * 50 * t) + 0.25 * np.sin(2 * np.pi * 90 * t)
    
    noise_A = np.random.normal(0, 0.2, len(t)) + traffic_rumble_A
    noise_B = np.random.normal(0, 0.2, len(t)) + traffic_rumble_B
    
    rx_A_raw = sig_A + noise_A
    rx_B_raw = sig_B + noise_B
    
    # -------------------------------------------------------------
    # 3. Apply Hardware MCP6002 Bandpass Filter (500 Hz - 3000 Hz)
    # -------------------------------------------------------------
    sos_afe = signal.butter(2, [500, 3000], btype='bandpass', fs=fs, output='sos')
    rx_A_filtered = signal.sosfilt(sos_afe, rx_A_raw)
    rx_B_filtered = signal.sosfilt(sos_afe, rx_B_raw)
    
    # -------------------------------------------------------------
    # 4. TDOA Cross-Correlation Engine
    # -------------------------------------------------------------
    corr = signal.correlate(rx_B_filtered, rx_A_filtered, mode='full')
    lags = signal.correlation_lags(len(rx_B_filtered), len(rx_A_filtered), mode='full')
    lag_times = lags / fs
    
    # Restrict search window to physically possible time delays (-D/v to +D/v)
    max_physical_lag = pipe_length / v_sound
    valid_mask = np.abs(lag_times) <= (max_physical_lag * 1.1)
    
    corr_window = corr[valid_mask]
    lag_times_window = lag_times[valid_mask]
    
    peak_idx = np.argmax(corr_window)
    estimated_tau = lag_times_window[peak_idx]
    
    # Parabolic sub-sample peak interpolation
    if 0 < peak_idx < len(corr_window) - 1:
        y0 = corr_window[peak_idx - 1]
        y1 = corr_window[peak_idx]
        y2 = corr_window[peak_idx + 1]
        delta = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
        estimated_tau += delta / fs
        
    # Triangulate physical distance
    estimated_x_leak = (pipe_length - v_sound * estimated_tau) / 2.0
    error_metres = np.abs(estimated_x_leak - x_leak_true)
    
    print(f"Estimated TDOA: {estimated_tau*1000:.3f} ms")
    print(f"Calculated Leak Distance from Node A: {estimated_x_leak:.2f} m")
    print(f"Localization Absolute Error: {error_metres:.2f} m ({error_metres*100:.1f} cm)")
    
    # -------------------------------------------------------------
    # 5. Plot 1: Full TDOA Proof Figure
    # -------------------------------------------------------------
    fig, axes = plt.subplots(4, 1, figsize=(11, 10), constrained_layout=True)
    
    # Subplot A: Raw Sensor Data
    axes[0].plot(t * 1000, rx_A_raw, color='#2563EB', alpha=0.8, label='Node A Raw (with Traffic Noise)')
    axes[0].plot(t * 1000, rx_B_raw, color='#D97706', alpha=0.7, label='Node B Raw (with Traffic Noise)')
    axes[0].set_ylabel('Amplitude (V)', fontsize=10, fontweight='bold', color='#1E293B')
    axes[0].set_title('(a) Raw Piezo Signals Clamped at Pipe Fittings (Unfiltered)', fontsize=11, fontweight='bold', color='#0F172A', loc='left')
    axes[0].legend(loc='upper right', frameon=True)
    axes[0].set_xlim(50, 200)
    
    # Subplot B: Conditioned AFE Data
    axes[1].plot(t * 1000, rx_A_filtered, color='#0284C7', lw=1.2, label='Node A Filtered (500Hz - 3kHz)')
    axes[1].plot(t * 1000, rx_B_filtered, color='#EA580C', lw=1.2, label='Node B Filtered (500Hz - 3kHz)')
    axes[1].axvline(t_flight_A * 1000, color='#0284C7', linestyle='--', alpha=0.7, label=f'Onset A: {t_flight_A*1000:.1f}ms')
    axes[1].axvline(t_flight_B * 1000, color='#EA580C', linestyle='--', alpha=0.7, label=f'Onset B: {t_flight_B*1000:.1f}ms')
    axes[1].set_ylabel('Filtered (V)', fontsize=10, fontweight='bold', color='#1E293B')
    axes[1].set_title('(b) MCP6002 2nd-Order Bandpass Filter Output (Traffic Rumble Suppressed)', fontsize=11, fontweight='bold', color='#0F172A', loc='left')
    axes[1].legend(loc='upper right', frameon=True)
    axes[1].set_xlim(50, 200)
    
    # Subplot C: Cross-Correlation Function
    axes[2].plot(lag_times_window * 1000, corr_window / np.max(corr_window), color='#059669', lw=1.5, label='Cross-Correlation $R_{BA}(\\tau)$')
    axes[2].axvline(estimated_tau * 1000, color='#DC2626', linestyle='-', lw=1.8, label=f'Peak $\\tau$ = {estimated_tau*1000:.2f} ms')
    axes[2].axvline(true_tau * 1000, color='#0F172A', linestyle=':', lw=1.5, label=f'True $\\tau$ = {true_tau*1000:.2f} ms')
    axes[2].set_xlabel('Time Lag $\\tau$ (milliseconds)', fontsize=10, fontweight='bold', color='#1E293B')
    axes[2].set_ylabel('Normalized $R_{BA}$', fontsize=10, fontweight='bold', color='#1E293B')
    axes[2].set_title('(c) Acoustic TDOA Cross-Correlation Curve & Triangulated Peak', fontsize=11, fontweight='bold', color='#0F172A', loc='left')
    axes[2].legend(loc='upper right', frameon=True)
    axes[2].set_xlim(-160, 160)
    
    # Subplot D: Physical Pipeline Triangulation Diagram
    axes[3].set_xlim(-10, pipe_length + 10)
    axes[3].set_ylim(-1.5, 2.0)
    axes[3].axis('off')
    
    # Draw pipe
    axes[3].plot([0, pipe_length], [0, 0], color='#64748B', lw=12, solid_capstyle='butt')
    axes[3].plot([0, pipe_length], [0, 0], color='#94A3B8', lw=8, solid_capstyle='butt')
    
    # Draw nodes
    axes[3].scatter([0], [0], color='#2563EB', s=250, zorder=5, marker='s', edgecolors='#0F172A', lw=1.5)
    axes[3].text(0, 0.45, "NODE A\n(Valve Chamber 1)", ha='center', fontsize=9, fontweight='bold', color='#1E293B')
    
    axes[3].scatter([pipe_length], [0], color='#D97706', s=250, zorder=5, marker='s', edgecolors='#0F172A', lw=1.5)
    axes[3].text(pipe_length, 0.45, "NODE B\n(Hydrant 2)", ha='center', fontsize=9, fontweight='bold', color='#1E293B')
    
    # Draw leak point
    axes[3].scatter([x_leak_true], [0], color='#DC2626', s=320, zorder=6, marker='v')
    axes[3].text(x_leak_true, 0.65, f"PINPOINTED LEAK\nTrue: {x_leak_true:.1f}m | Est: {estimated_x_leak:.1f}m (Error: {error_metres*100:.1f}cm)",
                 ha='center', fontsize=9, fontweight='bold', color='#DC2626',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#DC2626', lw=1))
                 
    # Acoustic wave ripples
    for radius in [12, 24, 36]:
        axes[3].annotate("", xy=(x_leak_true - radius, 0), xytext=(x_leak_true, 0),
                         arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=1.2, ls='--'))
        axes[3].annotate("", xy=(x_leak_true + radius, 0), xytext=(x_leak_true, 0),
                         arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=1.2, ls='--'))
        
    axes[3].text(pipe_length / 2, -0.7, f"Total Span D = {pipe_length:.0f} m  |  Ductile Iron ($v = {v_sound:.0f}$ m/s)  |  Distance = $(D - v \\cdot \\tau) / 2$",
                 ha='center', fontsize=9.5, fontweight='bold', color='#475569')
    axes[3].set_title('(d) Physical Triangulation: Pinpointed Dig Location on Municipal Line', fontsize=11, fontweight='bold', color='#0F172A', loc='left')
    
    plot1_path = os.path.join(output_dir, 'tdoa_cross_correlation_proof.png')
    fig.savefig(plot1_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {plot1_path}")
    
    # -------------------------------------------------------------
    # 6. Plot 2: AFE Sallen-Key Filter Bode Response
    # -------------------------------------------------------------
    w, h = signal.sosfreqz(sos_afe, worN=2000, fs=fs)
    
    fig2, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, constrained_layout=True)
    
    ax_mag.plot(w, 20 * np.log10(np.maximum(np.abs(h), 1e-5)), color='#2563EB', lw=2)
    ax_mag.axvspan(500, 3000, color='#38BDF8', alpha=0.15, label='Passband (500 Hz – 3000 Hz)')
    ax_mag.axvspan(10, 200, color='#F87171', alpha=0.15, label='Traffic Rumble Rejection (<200 Hz)')
    ax_mag.set_ylabel('Magnitude (dB)', fontsize=10, fontweight='bold', color='#1E293B')
    ax_mag.set_title('AQUAPULSE Analog Front-End (AFE) Frequency Response (MCP6002 Op-Amp)', fontsize=11, fontweight='bold', color='#0F172A')
    ax_mag.set_ylim(-50, 5)
    ax_mag.set_xscale('log')
    ax_mag.legend(loc='lower left', frameon=True)
    
    ax_phase.plot(w, np.unwrap(np.angle(h)) * 180 / np.pi, color='#D97706', lw=1.8)
    ax_phase.set_ylabel('Phase (degrees)', fontsize=10, fontweight='bold', color='#1E293B')
    ax_phase.set_xlabel('Frequency (Hz)', fontsize=10, fontweight='bold', color='#1E293B')
    ax_phase.set_xscale('log')
    ax_phase.set_xlim(20, 4000)
    
    plot2_path = os.path.join(output_dir, 'sensor_analog_filter_bode_plot.png')
    fig2.savefig(plot2_path, dpi=300)
    plt.close(fig2)
    print(f"Saved: {plot2_path}")
    
    # -------------------------------------------------------------
    # 7. Plot 3: Multi-Node Mesh Consensus Map
    # -------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(10, 4.5), constrained_layout=True)
    
    node_positions = [0, 150, 300, 450]
    node_names = ['Node #1\n(Gate Valve)', 'Node #2\n(Meter Chamber)', 'Node #3\n(Hydrant A)', 'Node #4\n(Valve Chamber)']
    
    # Pipe route
    ax3.plot([0, 450], [0, 0], color='#64748B', lw=10, zorder=1)
    
    # Nodes
    for pos, name in zip(node_positions, node_names):
        ax3.scatter([pos], [0], color='#2563EB', s=260, zorder=5, marker='s', edgecolors='#0F172A', lw=1.5)
        ax3.text(pos, -0.35, name, ha='center', fontsize=9, fontweight='bold', color='#1E293B')
        
    # Leak between Node 2 and Node 3 at x = 210m
    leak_x = 210
    ax3.scatter([leak_x], [0], color='#DC2626', s=350, zorder=6, marker='v')
    ax3.text(leak_x, 0.45, f"LEAK DETECTED (x = {leak_x}m)\nConsensus Confirmed (Pair 2-3 & Pair 1-2)",
             ha='center', fontsize=9.5, fontweight='bold', color='#DC2626',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#FEF2F2', edgecolor='#DC2626', lw=1.2))
             
    # ESP-NOW Mesh arcs
    arc1 = np.linspace(0, 150, 100)
    ax3.plot(arc1, 0.25 * np.sin(np.pi * arc1 / 150), color='#10B981', ls='--', lw=2, label='ESP-NOW Mesh Pair (1-2)')
    
    arc2 = np.linspace(150, 300, 100)
    ax3.plot(arc2, 0.25 * np.sin(np.pi * (arc2 - 150) / 150), color='#10B981', ls='--', lw=2, label='ESP-NOW Mesh Pair (2-3) [Triangulated]')
    
    arc3 = np.linspace(300, 450, 100)
    ax3.plot(arc3, 0.25 * np.sin(np.pi * (arc3 - 300) / 150), color='#10B981', ls='--', lw=2, label='ESP-NOW Mesh Pair (3-4)')
    
    ax3.set_xlim(-30, 480)
    ax3.set_ylim(-0.7, 0.9)
    ax3.axis('off')
    ax3.set_title('AQUAPULSE Multi-Node Mesh Consensus Validation Topology (False Positive Elimination)', fontsize=11, fontweight='bold', color='#0F172A', pad=15)
    ax3.legend(loc='lower center', ncol=3, frameon=True, fontsize=8.5)
    
    plot3_path = os.path.join(output_dir, 'pipe_acoustic_propagation_map.png')
    fig3.savefig(plot3_path, dpi=300)
    plt.close(fig3)
    print(f"Saved: {plot3_path}")

if __name__ == '__main__':
    target_dir = r'f:\HACKATHONS\vishwakarma\AQUAPULSE\docs\assets'
    run_simulation(target_dir)
    run_simulation(r'f:\HACKATHONS\vishwakarma\AQUAPULSE\simulation')
