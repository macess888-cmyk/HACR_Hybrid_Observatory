from itertools import combinations


def extract_counts(data):
    epochs = data.get("epochs", [])
    total_epochs = len(epochs)

    region_counts = {}
    corridor_counts = {}

    for epoch in epochs:
        regions = sorted(epoch.get("regions", []))

        for region in regions:
            region_counts[region] = region_counts.get(region, 0) + 1

        for a, b in combinations(regions, 2):
            key = f"{a} ↔ {b}"
            corridor_counts[key] = corridor_counts.get(key, 0) + 1

    return total_epochs, region_counts, corridor_counts


def extract_fixed_points(data):
    total_epochs, region_counts, corridor_counts = extract_counts(data)

    if total_epochs == 0:
        return {
            "status": "UNKNOWN_HOLD",
            "total_epochs": 0,
            "fixed_points": [],
            "fixed_connectivity": [],
            "observer_mode": True
        }

    fixed_points = []
    fixed_connectivity = []

    for region, count in sorted(region_counts.items()):
        if count == total_epochs:
            fixed_points.append({
                "name": region,
                "type": "FIXED_POINT",
                "visible_epochs": count,
                "total_epochs": total_epochs,
                "stability": 1.0,
                "classification": "STRUCTURAL_ANCHOR"
            })

    for corridor, count in sorted(corridor_counts.items()):
        if count == total_epochs:
            fixed_connectivity.append({
                "name": corridor,
                "type": "FIXED_CONNECTIVITY",
                "visible_epochs": count,
                "total_epochs": total_epochs,
                "stability": 1.0,
                "classification": "CONNECTIVITY_ANCHOR"
            })

    return {
        "status": "FIXED_POINT_EXTRACTION_COMPLETE",
        "total_epochs": total_epochs,
        "fixed_points": fixed_points,
        "fixed_connectivity": fixed_connectivity,
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False
    }