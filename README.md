# nnids_pipeline (minimal)

Pipeline minimale autonoma per:
- download giorni CIC-IDS2018 da AWS S3
- estrazione archivi (.zip / .rar)
- generazione flow CSV con CICFlowMeter
- labeling da configs/attack_schedule.yaml
- cache per giorno in preprocessed_cache/<day>/

## Setup iniziale

Prerequisiti di sistema (Linux):

```bash
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk unrar p7zip-full
```

Setup Python:

```bash
cd nnids_pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

## Esecuzione

```bash
python main.py
```

Con giorni specifici:

```bash
python main.py --days Thursday-15-02-2018 Friday-16-02-2018
```

Forza rigenerazione cache giorni richiesti:

```bash
python main.py --force
```

## Output principali

- `preprocessed_cache/<day>/benign_records.csv`
- `preprocessed_cache/<day>/attack_records.csv`
- `preprocessed_cache/<day>/preprocessed.csv` (se cache preprocess abilitata)
