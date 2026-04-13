#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flow labeling using attack_schedule.yaml for the minimal pipeline."""

from datetime import datetime, time
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

def load_schedule(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)

def parse_time(t: str) -> time:
    return datetime.strptime(t, "%H:%M").time()


def _parse_timestamp(value: str) -> Optional[datetime]:
    """Parse CICFlowMeter timestamp values across common formats."""
    if not isinstance(value, str):
        return None

    formats = [
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S.%f",
        "%d/%m/%Y %I:%M:%S",
        "%d/%m/%Y %I:%M:%S %p",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]
    raw = value.strip()
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def _find_col(columns, candidates):
    lowered = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lowered:
            return lowered[cand.lower()]
    return None


def apply(df: pd.DataFrame, day: Optional[str] = None, schedule_yaml=None) -> pd.DataFrame:
    if df.empty:
        return df

    if schedule_yaml is None:
        from configs.settings import ATTACK_SCHEDULE_YAML
        schedule_yaml = ATTACK_SCHEDULE_YAML

    schedule = load_schedule(Path(schedule_yaml))

    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    ts_col = _find_col(df.columns, ["Timestamp", "timestamp", "Flow Start Time"])
    src_col = _find_col(df.columns, ["Src IP", "Source IP", "src_ip", "SrcIP"])
    dst_col = _find_col(df.columns, ["Dst IP", "Destination IP", "dst_ip", "DstIP"])

    if ts_col is None or src_col is None or dst_col is None:
        df["Label"] = "Benign"
        return df

    # Convert timestamp once.
    try:
        parsed = df[ts_col].astype(str).apply(_parse_timestamp)
        df["flow_time"] = parsed.apply(lambda x: x.time() if x is not None else None)
        df["flow_date"] = parsed.apply(lambda x: x.date() if x is not None else None)
    except Exception:
        df["Label"] = "Benign"
        return df

    df["Label"] = "Benign"
    src_ip = df[src_col].astype(str)
    dst_ip = df[dst_col].astype(str)

    if day:
        day_info = schedule.get(day)
        schedule_iter = [(day, day_info)] if day_info else []
    else:
        schedule_iter = list(schedule.items())

    for _, day_info in schedule_iter:
        if not day_info:
            continue

        date_obj = datetime.strptime(day_info["date"], "%Y-%m-%d").date()
        day_mask = df["flow_date"] == date_obj
        if not day_mask.any():
            continue

        for attack in day_info.get("attacks", []):
            label = attack["label"]
            start_t = parse_time(attack["start"])
            end_t = parse_time(attack["end"])
            attacker_ips = set(attack.get("attacker_ips", []))
            victim_ips = set(attack.get("victim_ips", []))

            time_mask = (df["flow_time"] >= start_t) & (df["flow_time"] <= end_t)
            day_and_time = day_mask & time_mask
            if not day_and_time.any():
                continue

            ip_mask = (
                src_ip.isin(attacker_ips)
                | dst_ip.isin(victim_ips)
                | src_ip.isin(victim_ips)
                | dst_ip.isin(attacker_ips)
            )

            final_mask = day_and_time & ip_mask
            df.loc[final_mask, "Label"] = label

    df = df.drop(columns=["flow_time", "flow_date"], errors="ignore")
    return df