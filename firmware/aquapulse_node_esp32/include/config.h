/**
 * AQUAPULSE: Embedded Firmware Configuration
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 * 
 * Target: ESP32-S3 Dual Core Xtensa LX7 (240 MHz)
 */

#ifndef AQUAPULSE_CONFIG_H
#define AQUAPULSE_CONFIG_H

#include <Arduino.h>

// -------------------------------------------------------------
// Pin Assignments
// -------------------------------------------------------------
#define PIN_I2C_SDA         4
#define PIN_I2C_SCL         5
#define PIN_ADC_ALERT       6    // ADS1115 Data Ready Interrupt
#define PIN_RTC_SQW         7    // DS3231 1Hz / 32kHz Microsecond Sync
#define PIN_STATUS_RGB      48   // Built-in WS2812B NeoPixel
#define PIN_BATTERY_SENSE   1    // ADC1 channel for battery voltage monitoring

// -------------------------------------------------------------
// I2C Device Addresses
// -------------------------------------------------------------
#define ADDR_ADS1115        0x48 // 16-Bit Precision ADC
#define ADDR_DS3231         0x68 // TCXO Precision Real-Time Clock
#define ADDR_ADXL345        0x53 // 3-Axis Auxiliary Accelerometer

// -------------------------------------------------------------
// Sampling & Signal Processing Dynamics
// -------------------------------------------------------------
#define SAMPLING_FREQ_HZ    8000 // 8 kHz effective sampling rate
#define RING_BUFFER_SIZE    2048 // Circular RAM buffer (~256 ms rolling window)
#define SNIPPET_SIZE        512  // Waveform snippet exchanged over ESP-NOW (64 ms)
#define MAX_LAG_SAMPLES     320  // Max cross-correlation search window (±40 ms)
#define RMS_WINDOW_SIZE     128  // Moving RMS noise-floor calculation window
#define THRESHOLD_SIGMA     3.5f // Energy multiplier above noise floor to trigger

// -------------------------------------------------------------
// Pipeline Acoustic Velocity Lookup Table (m/s)
// -------------------------------------------------------------
enum PipeMaterial {
    PIPE_DUCTILE_IRON = 0,
    PIPE_CAST_IRON    = 1,
    PIPE_STEEL        = 2,
    PIPE_PVC          = 3,
    PIPE_HDPE         = 4
};

static inline float getAcousticVelocity(PipeMaterial mat) {
    switch (mat) {
        case PIPE_DUCTILE_IRON: return 1250.0f; // m/s with pressurized water column
        case PIPE_CAST_IRON:    return 1150.0f;
        case PIPE_STEEL:        return 1350.0f;
        case PIPE_PVC:          return 450.0f;
        case PIPE_HDPE:         return 380.0f;
        default:                return 1200.0f;
    }
}

// -------------------------------------------------------------
// ESP-NOW Mesh Protocol Settings
// -------------------------------------------------------------
#define ESPNOW_CHANNEL      1
#define MESH_MAX_PEERS      8
#define CORRELATION_TIMEOUT 300 // ms: window to wait for neighbouring waveform

#endif // AQUAPULSE_CONFIG_H
