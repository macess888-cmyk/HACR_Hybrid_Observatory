from tools.observatory_core.fixed_point import extract_fixed_points


def extract_anchors(data):

    fixed = extract_fixed_points(data)

    anchors = []

    for item in fixed.get("fixed_points", []):

        anchors.append({
            "name": item["name"],
            "type": "ANCHOR",
            "classification": "STRUCTURAL_ANCHOR",
            "stability": item["stability"]
        })

    connectivity_anchors = []

    for item in fixed.get("fixed_connectivity", []):

        connectivity_anchors.append({
            "name": item["name"],
            "type": "CONNECTIVITY_ANCHOR",
            "stability": item["stability"]
        })

    return {
        "status": "ANCHOR_EXTRACTION_COMPLETE",
        "anchors": anchors,
        "connectivity_anchors": connectivity_anchors,
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False
    }