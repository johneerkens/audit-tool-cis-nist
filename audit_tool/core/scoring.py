from collections import defaultdict, Counter

STATUS_WEIGHTS = {
    "PASS": 0,
    "PARTIAL": 1,
    "NOT_ASSESSED": 2,
    "FAIL": 3
}

def calculate_asset_risk(status, weight, asset):
    if status == "PASS":
        return 0
    
    return (
        STATUS_WEIGHTS[status]
        * weight
        * asset["criticality"]
        * asset["exposure"]
    )

def summarize_assessment(controls, answers, assets):

    overall_counts = Counter()
    function_scores = defaultdict(int)

    control_results = []

    for control in controls:
        total_risk = 0

        for sg in control["safeguards"]:
            status = answers.get(sg["id"], "NOT_ASSESSED")

            for asset in assets:
                risk = calculate_asset_risk(
                    status,
                    weight=1,  # can tune later
                    asset=asset
                )

                total_risk += risk

            overall_counts[status] += 1
            function_scores[control["nist_function"]] += total_risk

        control_results.append({
            "control_id": control["id"],
            "name": control["name"],
            "total_risk": total_risk
        })

    return {
        "overall_counts": dict(overall_counts),
        "function_risk": dict(function_scores),
        "controls": control_results
    }