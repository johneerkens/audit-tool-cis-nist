from __future__ import annotations
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'cis_controls_v8_1.json'


def load_controls() -> list[dict]:
    with DATA_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def get_control(control_id: str) -> dict | None:
    controls = load_controls()
    for control in controls:
        if control['id'] == control_id:
            return control
    return None


def all_safeguards() -> list[dict]:
    rows = []
    for control in load_controls():
        for sg in control['safeguards']:
            rows.append({
                'control_id': control['id'],
                'control_name': control['name'],
                'nist_function': control['nist_function'],
                'nist_category': control['nist_category'],
                **sg,
            })
    return rows
