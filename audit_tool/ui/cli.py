from __future__ import annotations
import argparse
import json
from audit_tool.core.assets import load_assets
from pathlib import Path
from audit_tool.core.dataset import load_controls, all_safeguards
from audit_tool.core.scoring import summarize_assessment

VALID_STATUSES = {'PASS', 'PARTIAL', 'FAIL', 'NOT_ASSESSED'}


def _load_answers(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise SystemExit(f'Answers file not found: {path}')
    with p.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return {str(k): str(v).upper() for k, v in data.items()}


def cmd_list_controls(args):
    controls = load_controls()
    for control in controls:
        print(f"[{control['id']}] {control['name']} | NIST: {control['nist_function']} / {control['nist_category']} | safeguards: {len(control['safeguards'])}")


def cmd_show_control(args):
    controls = load_controls()
    control = next((c for c in controls if c['id'] == args.control_id), None)
    if not control:
        raise SystemExit(f'Control not found: {args.control_id}')
    print(f"CIS Control {control['id']}: {control['name']}")
    print(f"NIST mapping: {control['nist_function']} / {control['nist_category']}")
    print(control['description'])
    print('Safeguards:')
    for sg in control['safeguards']:
        print(f"  - {sg['id']}: {sg['title']}")


def cmd_export_dataset(args):
    rows = all_safeguards()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == 'json':
        output.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    else:
        import csv
        with output.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['control_id', 'control_name', 'nist_function', 'nist_category', 'id', 'title'])
            writer.writeheader()
            writer.writerows(rows)
    print(f'Exported dataset to {output}')


def cmd_assess(args):
    controls = load_controls()
    answers = _load_answers(args.answers)

    assets = load_assets()
    summary = summarize_assessment(controls, answers, assets)
    
    print('\nNIST function summary:')
    for fn, values in sorted(summary['functions'].items()):
        print(f"  - {fn}: maturity {values['maturity_pct']}% | pass={values['pass']} partial={values['partial']} fail={values['fail']} not_assessed={values['not_assessed']}")

    print('\nLowest-scoring controls:')
    worst = sorted(summary['controls'], key=lambda x: x['maturity_pct'])[: args.top]
    for item in worst:
        print(f"  - CIS {item['control_id']} {item['control_name']}: {item['maturity_pct']}%")

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2), encoding='utf-8')
        print(f'\nDetailed report written to {out}')


def cmd_interactive(args):
    controls = load_controls()
    answers = {}

    
    print('Interactive assessment mode. Enter PASS, PARTIAL, FAIL, or NOT_ASSESSED. Press Enter to keep NOT_ASSESSED.')
    for control in controls:
        print(f"\n=== CIS {control['id']} - {control['name']} ===")
        for sg in control['safeguards']:
            raw = input(f"{sg['id']} {sg['title']}: ").strip().upper() or 'NOT_ASSESSED'
            while raw not in VALID_STATUSES:
                raw = input('Invalid value. Use PASS, PARTIAL, FAIL, or NOT_ASSESSED: ').strip().upper() or 'NOT_ASSESSED'
            answers[sg['id']] = raw
    assets = load_assets()
    summary = summarize_assessment(controls, answers, assets)
    print(f"\nOverall maturity: {summary['overall']['maturity_pct']}%")
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'answers': answers, 'summary': summary}, indent=2), encoding='utf-8')
        print(f'Saved interactive assessment to {out}')


def build_parser():
    parser = argparse.ArgumentParser(prog='audit-tool', description='CIS v8.1 + NIST CSF 2.0 CLI starter for administrator-oriented audits')
    sub = parser.add_subparsers(dest='command', required=True)

    p1 = sub.add_parser('list-controls', help='Show all CIS controls and NIST mappings')
    p1.set_defaults(func=cmd_list_controls)

    p2 = sub.add_parser('show-control', help='Show one control with all safeguards')
    p2.add_argument('control_id', help='CIS control id, e.g. 12')
    p2.set_defaults(func=cmd_show_control)

    p3 = sub.add_parser('export-dataset', help='Export the flattened safeguard dataset')
    p3.add_argument('--format', choices=['json', 'csv'], default='json')
    p3.add_argument('--output', required=True)
    p3.set_defaults(func=cmd_export_dataset)

    p4 = sub.add_parser('assess', help='Run a non-interactive assessment from a JSON answers file')
    p4.add_argument('--answers', required=True, help='Path to JSON answers file {"1.1":"PASS", ...}')
    p4.add_argument('--output', help='Write detailed JSON report')
    p4.add_argument('--top', type=int, default=5, help='Show top N weakest controls')
    p4.set_defaults(func=cmd_assess)

    p5 = sub.add_parser('interactive', help='Run the admin-friendly interactive CLI assessment')
    p5.add_argument('--output', help='Write answers and summary to JSON')
    p5.set_defaults(func=cmd_interactive)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
