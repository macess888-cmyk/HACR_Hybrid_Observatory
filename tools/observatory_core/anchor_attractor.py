from tools.observatory_core.anchor_basin import extract_anchor_basins


def extract_anchor_attractor(data):

    basin = extract_anchor_basins(data)

    attractor = {
        "name": "ANCHOR_ATTRACTOR",
        "classification": "ANCHOR_ATTRACTOR",
        "stability": 1.0,
        "source_anchor_count":
            basin["anchor_basin"]["anchor_count"],
        "source_connectivity_count":
            basin["anchor_basin"]["connectivity_count"]
    }

    return {
        "status": "ANCHOR_ATTRACTOR_EXTRACTION_COMPLETE",
        "anchor_attractor": attractor,
        "anchor_basin": basin["anchor_basin"],
        "anchor_core": basin["anchor_core"],
        "anchors": basin["anchors"],
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False
    }