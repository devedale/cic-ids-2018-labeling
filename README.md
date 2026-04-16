# synth-cic-ids-2018

## 1. Overview
An autonomous data augmentation pipeline for generating realistic, cyber-threat-intelligence (CTI) enriched Machine Learning datasets focused on Network Intrusion Detection systems. 

## 2. Objective
To solve the topological ambiguity in the original unadulterated [CIC-IDS-2018](https://registry.opendata.aws/cse-cic-ids2018/) dataset by strictly applying contemporary Host IDs obtained from verified CTI sources, thus preserving flow logic while updating IP attributions for accurate classification training.

## 3. Core Architecture
- **In-Memory S3 Pipeline**: Bypasses raw PCAP dependencies. Dynamically pulls precomputed Flow Data (`..._TrafficForML_CICFlowMeter.csv`) from AWS S3.
- **CTI Integration Module**: Extracts current malicious/benign IPs through Regex string matching against active GitHub threat-intelligence repositories.
- **Topological Logic Engine**: 
  - Malicious records are reassigned `Src IP` headers via 100% confidence CTI blocklists.
  - Benign records orchestrate synthetic public/private LAN scenarios adopting trusted, verified CTI whitelists.
  - RFC 1918 traffic bounds are structurally preserved.

## 4. Threat Intelligence Verticalization
This framework is strictly verticalized on the [`borestad`](https://github.com/borestad) repository ecosystem.
*   **Malicious Seed**: Extrapolated dynamically from `borestad/blocklist-abuseipdb` (AbuseIPDB 100% confidence offenders / 30-day active pool).
*   **Benign Seed**: Extrapolated dynamically from `borestad/iplists` (Whitelisted endpoints such as GoogleBot, Apple, BingBot, Office365).

## 5. Execution Protocol
**Dependencies**: Python 3.10+, `pandas`, `numpy`, `scikit-learn`, `boto3`.

### 5.1 Command Line interface
```bash
python main.py --days "Friday-02-03-2018"
```
### 5.2 Notebook Interface
Interactive experimentation is mapped in `pipeline_synth.ipynb`.

## 6. Output Artifacts
The ingestion processor outputs synthetic representations strictly isolated into `attack_records.csv` and `benign_records.csv` stored contextually under the `preprocessed_cache/<day>` directory.
# synth-cic-ids-2018
