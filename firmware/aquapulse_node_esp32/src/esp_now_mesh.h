/**
 * AQUAPULSE: ESP-NOW Mesh Protocol Header
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 */

#ifndef ESP_NOW_MESH_H
#define ESP_NOW_MESH_H

#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>
#include "config.h"

enum MeshMessageType {
    MSG_CANDIDATE_LEAK = 1,
    MSG_WAVEFORM_CHUNK = 2,
    MSG_CONSENSUS_VOTE = 3,
    MSG_HEARTBEAT      = 4
};

#pragma pack(push, 1)
struct MeshHeader {
    uint8_t msgType;
    uint8_t senderNodeId;
    uint32_t timestampMicroseconds;
    uint16_t sequenceId;
};

struct CandidateLeakPacket {
    MeshHeader header;
    float rmsEnergy;
    float peakAmplitude;
    uint16_t waveformSampleCount;
};

struct WaveformSnippetPacket {
    MeshHeader header;
    uint8_t chunkIndex;
    uint8_t totalChunks;
    int16_t samples[64]; // Sub-divided to stay well under 250-byte ESP-NOW MTU
};

struct ConsensusVotePacket {
    MeshHeader header;
    uint8_t targetNodePair[2];
    float estimatedDistanceMetres;
    float confidenceScore;
    bool isConfirmed;
};
#pragma pack(pop)

class MeshNetwork {
public:
    MeshNetwork();
    bool begin(uint8_t nodeId);
    void broadcastCandidateAlert(float rms, float peak, uint32_t timestampUs);
    void broadcastWaveformSnippet(const int16_t* samples, uint16_t count, uint32_t timestampUs);
    void broadcastConsensus(uint8_t nodeA, uint8_t nodeB, float dist, float score, bool confirmed);

    // Callbacks
    static void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status);
    static void onDataRecv(const esp_now_recv_info_t *recv_info, const uint8_t *data, int len);

private:
    uint8_t currentNodeId;
    uint8_t broadcastAddress[6];
};

extern MeshNetwork Mesh;

#endif // ESP_NOW_MESH_H
