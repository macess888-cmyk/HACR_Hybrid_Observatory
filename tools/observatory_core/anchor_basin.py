from tools.observatory_core.anchor import extract_anchors


def extract_anchor_basins(data):

    anchor_report = extract_anchors(data)

    anchors = anchor_report.get("anchors", [])
    connectivity = anchor_report.get("connectivity_anchors", [])

    basin_size = len(anchors)
    connectivity_size = len(connectivity)

    basin_strength = 0.0

    if basin_size > 0:
        basin_strength = (
            basin_size + connectivity_size
        ) / max(basin_size, 1)

    anchor_basin = {
        "name": "ANCHOR_BASIN_CORE",
        "anchor_count": basin_size,
        "connectivity_count": connectivity_size,
        "basin_strength": round(basin_strength, 4),
        "classification": "ANCHOR_BASIN"
    }

    anchor_core = {
        "name": "ANCHOR_CORE",
        "stability": 1.0,
        "classification": "ANCHOR_CORE"
    }

    return {
        "status": "ANCHOR_BASIN_EXTRACTION_COMPLETE",
        "anchor_basin": anchor_basin,
        "anchor_core": anchor_core,
        "anchors": anchors,
        "connectivity_anchors": connectivity,
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False
    }