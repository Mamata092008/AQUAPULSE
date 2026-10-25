/**
 * AQUAPULSE: TDOA Cross-Correlation Engine Implementation
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 */

#include "tdoa_correlator.h"
#include <math.h>

TDOACorrelator::TDOACorrelator() {
    memset(correlationBuffer, 0, sizeof(correlationBuffer));
}

TriangulationResult TDOACorrelator::correlateAndTriangulate(
    const int16_t* signalA,
    const int16_t* signalB,
    uint16_t length,
    float pipeSpan,
    float acousticVel
) {
    TriangulationResult result;
    result.isValid = false;
    result.distanceFromNodeA = 0.0f;
    result.timeLagSeconds = 0.0f;
    result.normalizedScore = 0.0f;

    if (length == 0 || pipeSpan <= 0.0f || acousticVel <= 0.0f) {
        return result;
    }

    // 1. Calculate signal energies for normalization
    double energyA = 0.0;
    double energyB = 0.0;
    for (uint16_t i = 0; i < length; i++) {
        energyA += (double)signalA[i] * (double)signalA[i];
        energyB += (double)signalB[i] * (double)signalB[i];
    }
    double normFactor = sqrt(energyA * energyB);
    if (normFactor < 1e-6) {
        return result; // Flatline / zero energy
    }

    // 2. Compute cross-correlation over physical lag window [-MAX_LAG, +MAX_LAG]
    int maxPhysicalLag = (int)ceil((pipeSpan / acousticVel) * SAMPLING_FREQ_HZ * 1.15f);
    if (maxPhysicalLag > MAX_LAG_SAMPLES) {
        maxPhysicalLag = MAX_LAG_SAMPLES;
    }

    float maxCorrelation = -1.0e12f;
    int bestLagIndex = 0;

    for (int lag = -maxPhysicalLag; lag <= maxPhysicalLag; lag++) {
        double sum = 0.0;
        int count = 0;

        for (int i = 0; i < length; i++) {
            int j = i + lag;
            if (j >= 0 && j < length) {
                sum += (double)signalB[j] * (double)signalA[i];
                count++;
            }
        }

        int bufferIdx = lag + MAX_LAG_SAMPLES;
        float r_val = (count > 0) ? (float)(sum / normFactor) : 0.0f;
        correlationBuffer[bufferIdx] = r_val;

        if (r_val > maxCorrelation) {
            maxCorrelation = r_val;
            bestLagIndex = bufferIdx;
        }
    }

    int bestLag = bestLagIndex - MAX_LAG_SAMPLES;
    float refinedLag = (float)bestLag;

    // 3. Sub-Sample Interpolation via 3-point Parabolic Fitting
    if (bestLagIndex > 0 && bestLagIndex < (MAX_LAG_SAMPLES * 2)) {
        float y_prev = correlationBuffer[bestLagIndex - 1];
        float y_peak = correlationBuffer[bestLagIndex];
        float y_next = correlationBuffer[bestLagIndex + 1];
        float denom = (y_prev - 2.0f * y_peak + y_next);
        
        if (fabsf(denom) > 1e-6f) {
            float delta = 0.5f * (y_prev - y_next) / denom;
            if (fabsf(delta) < 1.0f) {
                refinedLag += delta;
            }
        }
    }

    // 4. Time Difference of Arrival (tau) and Distance Calculation
    float tau = refinedLag / (float)SAMPLING_FREQ_HZ;
    // Formula: Distance from Node A = (D - v * tau) / 2
    float calculatedDistance = (pipeSpan - acousticVel * tau) / 2.0f;

    result.timeLagSeconds = tau;
    result.distanceFromNodeA = calculatedDistance;
    result.normalizedScore = maxCorrelation;

    // Validate: Distance must lie between 0 and pipeSpan, and correlation coefficient r > 0.45
    if (calculatedDistance >= -1.0f && calculatedDistance <= (pipeSpan + 1.0f) && maxCorrelation >= 0.45f) {
        result.isValid = true;
        // Clamp to physical pipeline boundaries
        if (result.distanceFromNodeA < 0.0f) result.distanceFromNodeA = 0.0f;
        if (result.distanceFromNodeA > pipeSpan) result.distanceFromNodeA = pipeSpan;
    }

    return result;
}
