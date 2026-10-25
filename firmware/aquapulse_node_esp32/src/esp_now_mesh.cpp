/**
 * AQUAPULSE: ESP-NOW Mesh Protocol Implementation
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 */

#include "esp_now_mesh.h"

MeshNetwork Mesh;

MeshNetwork::MeshNetwork() : currentNodeId(1) {
    memset(broadcastAddress, 0xFF, 6); // Broadcast MAC: FF:FF:FF:FF:FF:FF
}

bool MeshNetwork::begin(uint8_t nodeId) {
    currentNodeId = nodeId;
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    if (esp_now_init() != ESP_OK) {
        Serial.println("[MESH] ERROR: Failed to initialize ESP-NOW");
        return false;
    }

    esp_now_register_send_cb(MeshNetwork::onDataSent);
    esp_now_register_recv_cb(MeshNetwork::onDataRecv);

    // Register broadcast peer
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, broadcastAddress, 6);
    peerInfo.channel = ESPNOW_CHANNEL;
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("[MESH] ERROR: Failed to add broadcast peer");
        return false;
    }

    Serial.printf("[MESH] Initialized successfully. Node ID: %d | MAC: %s\n",
                  currentNodeId, WiFi.macAddress().c_str());
    return true;
}

void MeshNetwork::broadcastCandidateAlert(float rms, float peak, uint32_t timestampUs) {
    CandidateLeakPacket pkt;
    pkt.header.msgType = MSG_CANDIDATE_LEAK;
    pkt.header.senderNodeId = currentNodeId;
    pkt.header.timestampMicroseconds = timestampUs;
    pkt.header.sequenceId = (uint16_t)(millis() & 0xFFFF);
    pkt.rmsEnergy = rms;
    pkt.peakAmplitude = peak;
    pkt.waveformSampleCount = SNIPPET_SIZE;

    esp_now_send(broadcastAddress, (uint8_t*)&pkt, sizeof(pkt));
}

void MeshNetwork::broadcastWaveformSnippet(const int16_t* samples, uint16_t count, uint32_t timestampUs) {
    // 512 samples divided into 8 chunks of 64 samples
    const uint8_t CHUNK_SIZE = 64;
    uint8_t totalChunks = (count + CHUNK_SIZE - 1) / CHUNK_SIZE;

    for (uint8_t c = 0; c < totalChunks; c++) {
        WaveformSnippetPacket pkt;
        pkt.header.msgType = MSG_WAVEFORM_CHUNK;
        pkt.header.senderNodeId = currentNodeId;
        pkt.header.timestampMicroseconds = timestampUs;
        pkt.header.sequenceId = (uint16_t)(millis() & 0xFFFF);
        pkt.chunkIndex = c;
        pkt.totalChunks = totalChunks;

        uint16_t offset = c * CHUNK_SIZE;
        uint16_t copyCount = (offset + CHUNK_SIZE <= count) ? CHUNK_SIZE : (count - offset);
        memcpy(pkt.samples, &samples[offset], copyCount * sizeof(int16_t));

        esp_now_send(broadcastAddress, (uint8_t*)&pkt, sizeof(pkt));
        delayMicroseconds(200); // Prevent radio buffer overflow
    }
}

void MeshNetwork::broadcastConsensus(uint8_t nodeA, uint8_t nodeB, float dist, float score, bool confirmed) {
    ConsensusVotePacket pkt;
    pkt.header.msgType = MSG_CONSENSUS_VOTE;
    pkt.header.senderNodeId = currentNodeId;
    pkt.header.timestampMicroseconds = micros();
    pkt.header.sequenceId = (uint16_t)(millis() & 0xFFFF);
    pkt.targetNodePair[0] = nodeA;
    pkt.targetNodePair[1] = nodeB;
    pkt.estimatedDistanceMetres = dist;
    pkt.confidenceScore = score;
    pkt.isConfirmed = confirmed;

    esp_now_send(broadcastAddress, (uint8_t*)&pkt, sizeof(pkt));
}

void MeshNetwork::onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    // Non-blocking telemetry
}

void MeshNetwork::onDataRecv(const esp_now_recv_info_t *recv_info, const uint8_t *data, int len) {
    if (len < (int)sizeof(MeshHeader)) return;
    const MeshHeader* hdr = (const MeshHeader*)data;

    // Discard packets sent by self
    if (hdr->senderNodeId == Mesh.currentNodeId) return;

    switch (hdr->msgType) {
        case MSG_CANDIDATE_LEAK: {
            const CandidateLeakPacket* pkt = (const CandidateLeakPacket*)data;
            Serial.printf("[MESH] Candidate alert received from Node %d! RMS: %.2f | TS: %u us\n",
                          pkt->header.senderNodeId, pkt->rmsEnergy, pkt->header.timestampMicroseconds);
            break;
        }
        case MSG_CONSENSUS_VOTE: {
            const ConsensusVotePacket* pkt = (const ConsensusVotePacket*)data;
            Serial.printf("[MESH] Consensus vote from Node %d: Pair (%d-%d) -> Dist: %.2f m | Conf: %.2f | Confirmed: %s\n",
                          pkt->header.senderNodeId, pkt->targetNodePair[0], pkt->targetNodePair[1],
                          pkt->estimatedDistanceMetres, pkt->confidenceScore, pkt->isConfirmed ? "YES" : "NO");
            break;
        }
        default:
            break;
    }
}
