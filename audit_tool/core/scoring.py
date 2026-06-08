from __future__ import annotations
from collections import Counter, defaultdict

STATUS_WEIGHTS = {
    'PASS': 0,
    'PARTIAL': 1,
    'NOT_ASSESSED': 2,
    'FAIL': 3,
}


def summarize_assessment(controls: list[dict], answers: dict[str, str]) -> dict:
    control_results = []
    function_totals = defaultdict(lambda: {'pass': 0, 'partial': 0, 'fail': 0, 'not_assessed': 0, 'score': 0, 'items': 0})
    overall_counts = Counter()

    for control in controls:
        safeguard_results = []
        total_score = 0
        for sg in control['safeguards']:
            status = answers.get(sg['id'], 'NOT_ASSESSED').upper()
            if status not in STATUS_WEIGHTS:
                status = 'NOT_ASSESSED'
            score = STATUS_WEIGHTS[status]
            safeguard_results.append({
                'id': sg['id'],
                'title': sg['title'],
                'status': status,
                'score': score,
            })
            total_score += score
            bucket = status.lower()
            if bucket == 'not_assessed':
                function_totals[control['nist_function']]['not_assessed'] += 1
            else:
                function_totals[control['nist_function']][bucket] += 1
            function_totals[control['nist_function']]['score'] += score
            function_totals[control['nist_function']]['items'] += 1
            overall_counts[status] += 1

        max_score = len(control['safeguards']) * max(STATUS_WEIGHTS.values())
        maturity_pct = round(100 * (1 - (total_score / max_score)), 2) if max_score else 100
        control_results.append({
            'control_id': control['id'],
            'control_name': control['name'],
            'nist_function': control['nist_function'],
            'nist_category': control['nist_category'],
            'maturity_pct': maturity_pct,
            'safeguards': safeguard_results,
        })

    function_summary = {}
    for fn, values in function_totals.items():
        max_score = values['items'] * max(STATUS_WEIGHTS.values())
        maturity_pct = round(100 * (1 - (values['score'] / max_score)), 2) if max_score else 100
        function_summary[fn] = {
            **values,
            'maturity_pct': maturity_pct,
        }

    total_items = sum(overall_counts.values())
    max_score = total_items * max(STATUS_WEIGHTS.values())
    total_score = sum(STATUS_WEIGHTS[k] * v for k, v in overall_counts.items())
    return {
        'overall': {
            'items': total_items,
            'status_counts': dict(overall_counts),
            'maturity_pct': round(100 * (1 - (total_score / max_score)), 2) if max_score else 100,
        },
        'functions': function_summary,
        'controls': control_results,
    }
