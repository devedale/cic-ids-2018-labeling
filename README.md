# cic-ids-2018-labeling

Autonomous end-to-end data processing pipeline for the CIC-IDS2018 network intrusion detection dataset.

## Overview

The pipeline reproduces the full ingestion-to-features workflow from raw network captures to labelled, preprocessed feature vectors suitable for machine learning experiments:

| Stage | Description |
|-------|-------------|
| **Ingestion** | Downloads daily PCAP archives from the public AWS S3 bucket `cse-cic-ids2018` |
| **Flow extraction** | Generates per-flow CSV files via CICFlowMeter (requires Java 8) |
| **Labeling** | Assigns per-row attack labels using Apache Spark (map-reduce), driven by `configs/attack_schedule.yaml` |
| **Preprocessing** | Applies feature selection, missing-value imputation, standard scaling, and optional stratified sampling |
| **Cache** | Persists per-day results to `preprocessed_cache/<day>/` to avoid redundant reprocessing |

## Repository Structure

```
nnids_pipeline/
├── main.py                        # CLI entry point
├── setup.sh                       # Automated environment setup script
├── requirements.txt
├── configs/
│   ├── settings.py                # Paths, day selection, and pipeline parameters
│   └── attack_schedule.yaml       # Per-day attack time windows and IP ranges
├── core/
│   ├── ingestion.py               # S3 download → archive extraction → CICFlowMeter
│   ├── labeling.py                # Spark map-reduce: assigns attack/benign labels
│   └── preprocessing.py          # Feature engineering and normalisation
├── data/                          # Raw archives and PCAPs (gitignored)
└── preprocessed_cache/            # Labelled output CSVs (gitignored)
```

## Quick Start

Clone the repository and run the setup script:
>>>>>>> 51ad0cb (update readme)
# cic-ids-2018-labeling

Autonomous end-to-end data processing pipeline for the CIC-IDS2018 network intrusion detection dataset.

## Overview

The pipeline reproduces the full ingestion-to-features workflow from raw network captures to labelled, preprocessed feature vectors suitable for machine learning experiments:

| Stage | Description |
|-------|-------------|
| **Ingestion** | Downloads daily PCAP archives from the public AWS S3 bucket `cse-cic-ids2018` |
| **Flow extraction** | Generates per-flow CSV files via CICFlowMeter (requires Java 8) |
| **Labeling** | Assigns per-row attack labels using Apache Spark (map-reduce), driven by `configs/attack_schedule.yaml` |
| **Preprocessing** | Applies feature selection, missing-value imputation, standard scaling, and optional stratified sampling |
| **Cache** | Persists per-day results to `preprocessed_cache/<day>/` to avoid redundant reprocessing |

## Repository Structure

```
nnids_pipeline/
├── main.py                        # CLI entry point
├── setup.sh                       # Automated environment setup script
├── requirements.txt
├── configs/
│   ├── settings.py                # Paths, day selection, and pipeline parameters
│   └── attack_schedule.yaml       # Per-day attack time windows and IP ranges
├── core/
│   ├── ingestion.py               # S3 download → archive extraction → CICFlowMeter
│   ├── labeling.py                # Spark map-reduce: assigns attack/benign labels
│   └── preprocessing.py          # Feature engineering and normalisation
├── data/                          # Raw archives and PCAPs (gitignored)
└── preprocessed_cache/            # Labelled output CSVs (gitignored)
```

## Quick Start

Clone the repository and run the setup script:
>>>>>>> 51ad0cb (update readme)

### 5.1 Command Line interface
```bash
python main.py --days "Friday-02-03-2018"
```
### 5.2 Notebook Interface
Interactive experimentation is mapped in `pipeline_synth.ipynb`.

<<<<<<< HEAD
## 6. Output Artifacts
The ingestion processor outputs synthetic representations strictly isolated into `attack_records.csv` and `benign_records.csv` stored contextually under the `preprocessed_cache/<day>` directory.
# synth-cic-ids-2018
=======
`setup.sh` performs the following steps:
1. Installs system dependencies (`openjdk-8-jdk`, `openjdk-17-jdk`, `unrar`, `p7zip-full`)
2. Creates a Python virtual environment at `.venv` (skipped if it already exists)
3. Installs Python packages from `requirements.txt`
4. Runs a PySpark smoke-test to verify the installation

> **Requirements**: Linux, Python ≥ 3.8, `sudo` available.

## Usage

Run with the days configured in `configs/settings.py`:

```bash
python main.py
```

Process specific days:

```bash
python main.py --days Thursday-15-02-2018 Friday-16-02-2018
```

Force reprocessing, ignoring any existing cache:

```bash
python main.py --force
```

Persist the preprocessed DataFrame to disk:

```bash
python main.py --cache
```

### CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--days` | from `settings.py` | Days to process |
| `--force` | `False` | Discard cache and regenerate all outputs |
| `--sample` | `20000` | Maximum sample size per run (0 = no limit) |
| `--cache` / `--no-cache` | `False` | Save `preprocessed.csv` to the cache directory |

## Dataset Days

Active days are configured via the `DAYS` list in `configs/settings.py`.
The CIC-IDS2018 dataset spans the following capture sessions:

| Day | Attack Types |
|-----|-------------|
| Wednesday-14-02-2018 | FTP-BruteForce, SSH-BruteForce |
| Thursday-15-02-2018  | DoS-GoldenEye, DoS-Slowloris |
| Friday-16-02-2018    | DoS-SlowHTTPTest, DoS-Hulk |
| Tuesday-20-02-2018   | DDoS-LOIC-HTTP, DDoS-LOIC-UDP |
| Wednesday-21-02-2018 | DDoS-LOIC-UDP, DDoS-HOIC |
| Thursday-22-02-2018  | Web-BruteForce, Web-XSS, Web-SQLi |
| Friday-23-02-2018    | Web attacks (continued) |
| Wednesday-28-02-2018 | Infiltration |
| Thursday-01-03-2018  | Infiltration (continued) |
| Friday-02-03-2018    | Bot |

## Output Files

Each processed day produces the following files under `preprocessed_cache/<day>/`:

| File | Contents |
|------|----------|
| `benign_records.csv` | Labelled benign network flows |
| `attack_records.csv` | Labelled attack network flows |
| `preprocessed.csv`   | Scaled and encoded feature matrix (only with `--cache`) |

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `run_pipeline.ipynb` | Minimal end-to-end execution on Jupyter or Google Colab |
| `cicids2018_pipeline.ipynb` | Full Colab walkthrough with system setup, CICFlowMeter build, and pipeline run |
>>>>>>> 51ad0cb (update readme)
