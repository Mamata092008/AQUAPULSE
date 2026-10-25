/**
 * AQUAPULSE: Main Node Firmware Entry Point
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 * 
 * FreeRTOS Dual-Core Architecture:
 * - Core 0 (Task_Sampling): High-speed ADS1115 ADC reading, Ring Buffer & RMS Triggering
 * - Core 1 (Task_NetworkAndTDOA): ESP-NOW Mesh Communication, Cross-Correlation & Consensus
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <RTClib.h>
#include <Adafruit_ADXL345_U.h>
#include <FastLED.h>

#include "config.h"
#include "tdoa_correlator.h"
#include "esp_now_mesh.h"

// Hardware Instances
Adafruit_ADS1115 ads;
RTC_DS3231 rtc;
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
CRGB leds[1];
TDOACorrelator correlator;

// Circular Sample Buffer
int16_t ringBuffer[RING_BUFFER_SIZE];
volatile uint16_t headIdx = 0;
portMUX_TYPE bufferMux = portMUX_INITIALIZER_UNLOCKED;

// Snippet Queues
int16_t localSnippet[SNIPPET_SIZE];
int16_t remoteSnippet[SNIPPET_SIZE];
volatile bool remoteSnippetReady = false;
volatile uint32_t triggerTimestampUs = 0;

// Dynamic Noise Baseline
float movingRmsNoise = 50.0f;

// FreeRTOS Task Handles
TaskHandle_t TaskSamplingHandle;
TaskHandle_t TaskTDOAHandle;

// Status LED state helper
void setStatusLed(CRGB color) {
    leds[0] = color;
    FastLED.show();
}

/**
 * CORE 0: Real-time Audio / Acoustic Sampling & Anomaly Detection Task
 */
void Task_Sampling(void* pvParameters) {
    Serial.printf("[CORE 0] Sampling Engine active on Core %d\n", xPortGetCoreID());

    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(1); // 1 ms loop cadence

    while (true) {
        // 1. Read Differential AIN0-AIN1 from ADS1115
        int16_t rawSample = ads.readADC_Differential_0_1();

        // 2. Insert into Thread-Safe Circular RAM Buffer
        portENTER_CRITICAL(&bufferMux);
        ringBuffer[headIdx] = rawSample;
        headIdx = (headIdx + 1) % RING_BUFFER_SIZE;
        portEXIT_CRITICAL(&bufferMux);

        // 3. Compute Short-Time RMS Energy
        static uint16_t sampleCounter = 0;
        static int32_t accumEnergy = 0;
        accumEnergy += (int32_t)rawSample * (int32_t)rawSample;
        sampleCounter++;

        if (sampleCounter >= RMS_WINDOW_SIZE) {
            float currentRms = sqrtf((float)accumEnergy / (float)RMS_WINDOW_SIZE);
            accumEnergy = 0;
            sampleCounter = 0;

            // 4. Update dynamic baseline (exponential moving average: slow adapt)
            movingRmsNoise = 0.98f * movingRmsNoise + 0.02f * currentRms;

            // 5. Threshold Trigger Check (Candidate Leak Event)
            if (currentRms > (movingRmsNoise * THRESHOLD_SIGMA)) {
                triggerTimestampUs = micros();
                setStatusLed(CRGB::Amber);
                Serial.printf("[CORE 0] *** LEAK CANDIDATE TRIGGERED *** RMS: %.1f (Baseline: %.1f)\n",
                              currentRms, movingRmsNoise);

                // Copy the most recent SNIPPET_SIZE samples into localSnippet
                portENTER_CRITICAL(&bufferMux);
                uint16_t startIdx = (headIdx + RING_BUFFER_SIZE - SNIPPET_SIZE) % RING_BUFFER_SIZE;
                for (uint16_t s = 0; s < SNIPPET_SIZE; s++) {
                    localSnippet[s] = ringBuffer[(startIdx + s) % RING_BUFFER_SIZE];
                }
                portEXIT_CRITICAL(&bufferMux);

                // Broadcast alert and snippet over ESP-NOW mesh
                Mesh.broadcastCandidateAlert(currentRms, (float)rawSample, triggerTimestampUs);
                Mesh.broadcastWaveformSnippet(localSnippet, SNIPPET_SIZE, triggerTimestampUs);
            }
        }

        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

/**
 * CORE 1: Mesh Networking, TDOA Cross-Correlation & Multi-Pair Consensus Task
 */
void Task_NetworkAndTDOA(void* pvParameters) {
    Serial.printf("[CORE 1] TDOA & Mesh Engine active on Core %d\n", xPortGetCoreID());

    while (true) {
        // If a remote waveform snippet was received from neighbouring node
        if (remoteSnippetReady) {
            remoteSnippetReady = false;
            setStatusLed(CRGB::Blue);

            Serial.println("[CORE 1] Running TDOA Cross-Correlation Engine...");
            float pipeSpan = PIPE_SPAN_METRES;
            float vSound = getAcousticVelocity(PIPE_DUCTILE_IRON);

            TriangulationResult res = correlator.correlateAndTriangulate(
                localSnippet,
                remoteSnippet,
                SNIPPET_SIZE,
                pipeSpan,
                vSound
            );

            if (res.isValid) {
                setStatusLed(CRGB::Red); // Confirmed Leak!
                Serial.println("==================================================");
                Serial.println("[ALERT] >>> LEAK CONFIRMED VIA CROSS-CORRELATION <<<");
                Serial.printf("        Lag (tau): %.3f ms\n", res.timeLagSeconds * 1000.0f);
                Serial.printf("        Triangulated Position: %.2f metres from Node\n", res.distanceFromNodeA);
                Serial.printf("        Correlation Coefficient r: %.3f\n", res.normalizedScore);
                Serial.println("==================================================");

                // Broadcast consensus vote to network gateway
                Mesh.broadcastConsensus(NODE_ID, NODE_ID + 1, res.distanceFromNodeA, res.normalizedScore, true);
            } else {
                setStatusLed(CRGB::Green);
                Serial.printf("[CORE 1] Cross-correlation below confidence threshold (r = %.2f). Noise rejected.\n",
                              res.normalizedScore);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n========================================================");
    Serial.println("   AQUAPULSE: Non-Invasive Acoustic Sensor Node v1.2    ");
    Serial.println("   Team TECHTONICS | Vishwakarma Awards 2026-27 (IIT-H) ");
    Serial.println("========================================================");

    // 1. Initialize Status NeoPixel
    FastLED.addLeds<WS2812B, PIN_STATUS_RGB, GRB>(leds, 1);
    setStatusLed(CRGB::Cyan); // Booting

    // 2. Initialize Fast I2C Bus (400 kHz)
    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 400000);

    // 3. Initialize ADS1115 ADC
    if (!ads.begin(ADDR_ADS1115)) {
        Serial.println("[ADC] ERROR: ADS1115 not detected on I2C bus!");
    } else {
        ads.setGain(GAIN_ONE); // +/- 4.096V range (1 bit = 0.125mV)
        ads.setDataRate(RATE_ADS1115_860SPS);
        Serial.println("[ADC] ADS1115 16-Bit ADC calibrated & ready.");
    }

    // 4. Initialize DS3231 Precision RTC
    if (!rtc.begin()) {
        Serial.println("[RTC] ERROR: DS3231 not detected!");
    } else {
        rtc.writeSqwPinMode(DS3231_SquareWave1kHz);
        DateTime now = rtc.now();
        Serial.printf("[RTC] DS3231 TCXO Synced: %04d-%02d-%02d %02d:%02d:%02d\n",
                      now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
    }

    // 5. Initialize ADXL345 Accelerometer
    if (!accel.begin(ADDR_ADXL345)) {
        Serial.println("[ACCEL] ADXL345 not found, operating in single-transducer mode.");
    } else {
        accel.setRange(ADXL345_RANGE_2_G);
        Serial.println("[ACCEL] ADXL345 calibrated for multi-modal vibration validation.");
    }

    // 6. Initialize ESP-NOW Mesh Protocol
    Mesh.begin(NODE_ID);

    // 7. Spawn FreeRTOS Tasks pinned to Dual Cores
    xTaskCreatePinnedToCore(
        Task_Sampling,
        "Task_Sampling",
        4096,
        NULL,
        2, // High priority
        &TaskSamplingHandle,
        0  // Pin to Core 0
    );

    xTaskCreatePinnedToCore(
        Task_NetworkAndTDOA,
        "Task_NetworkAndTDOA",
        4096,
        NULL,
        1, // Normal priority
        &TaskTDOAHandle,
        1  // Pin to Core 1
    );

    setStatusLed(CRGB::Green); // Online & Listening
    Serial.println("[SYSTEM] All subsystems initialized. Listening for pipeline acoustic stress waves...\n");
}

void loop() {
    // Background supervisory heartbeat (every 10 seconds)
    static uint32_t lastHeartbeat = 0;
    if (millis() - lastHeartbeat > 10000) {
        lastHeartbeat = millis();
        Serial.printf("[HEALTH] Uptime: %lus | Noise Floor: %.1f | Free Heap: %d bytes\n",
                      millis() / 1000, movingRmsNoise, ESP.getFreeHeap());
    }
    delay(100);
}
