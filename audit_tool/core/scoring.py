from collections import defaultdict, Counter

STATUS_WEIGHTS = {
    "PASS": 0,
    "PARTIAL": 1,
    "NOT_ASSESSED": 2,
    "FAIL": 3
}

def calculate_asset_risk(status, asset):
    if status == "PASS":
        return 0

    return (
        STATUS_WEIGHTS[status]
        * asset["criticality"]
        * asset["exposure"]
    )

def summarize_assessment(controls, answers, assets):

    overall_counts = Counter()

    function_risk = defaultdict(int)
    asset_risk = defaultdict(int)

    control_results = []

    for control in controls:
        control_total = 0

        for sg in control["safeguards"]:
            status = answers.get(sg["id"], "NOT_ASSESSED")

            for asset in assets:
                risk = calculate_asset_risk(status, asset)

                # ✅ accumulate per asset
                asset_risk[asset["name"]] += risk

                # ✅ accumulate per NIST function
                function_risk[control["nist_function"]] += risk

                control_total += risk

            overall_counts[status] += 1

        control_results.append({
            "control_id": control["id"],
            "name": control["name"],
            "total_risk": control_total
        })

    return {
        "overall_counts": dict(overall_counts),
        "function_risk": dict(function_risk),
        "asset_risk": dict(asset_risk),   # ✅ NEW
        "controls": control_results
    }