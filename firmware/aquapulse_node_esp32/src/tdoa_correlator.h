/**
 * AQUAPULSE: TDOA Cross-Correlation Engine
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 */

#ifndef TDOA_CORRELATOR_H
#define TDOA_CORRELATOR_H

#include <Arduino.h>
#include "config.h"

struct TriangulationResult {
    float timeLagSeconds;     // Estimated Time Difference of Arrival (tau)
    float distanceFromNodeA;  // Calculated distance in metres from Node A
    float normalizedScore;    // Cross-correlation peak coefficient r in [0, 1]
    bool isValid;             // Whether correlation passed significance check
};

class TDOACorrelator {
public:
    TDOACorrelator();
    
    /**
     * Executes discrete cross-correlation R_xy(tau) between two synchronized 512-sample arrays.
     * Applies parabolic sub-sample peak interpolation to achieve millimeter-grade accuracy.
     * 
     * @param signalA Waveform recorded at Node A
     * @param signalB Waveform recorded at Node B
     * @param length Number of samples in each snippet (typically 512)
     * @param pipeSpan Distance D in metres between Node A and Node B
     * @param acousticVel Acoustic velocity v in m/s through pipe and water
     * @return TriangulationResult structure with distance and confidence
     */
    TriangulationResult correlateAndTriangulate(
        const int16_t* signalA,
        const int16_t* signalB,
        uint16_t length,
        float pipeSpan,
        float acousticVel
    );

private:
    float correlationBuffer[MAX_LAG_SAMPLES * 2 + 1];
};

#endif // TDOA_CORRELATOR_H
