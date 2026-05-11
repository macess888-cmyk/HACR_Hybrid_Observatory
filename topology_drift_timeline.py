import json
import os

INPUT_FILE = "Inputs/topology_timeline_case.json"
OUTPUT_FILE = "Outputs/topology_timeline_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

snapshots = data.get("snapshots", [])

events = []
status = "STABLE"

previous_edges = set()

for snapshot in snapshots:
    timestamp = snapshot.get("timestamp")
    edges = snapshot.get("edges", [])

    current_edges = set(
        (edge.get("from"), edge.get("to"))
        for edge in edges
    )

    added = current_edges - previous_edges
    removed = previous_edges - current_edges

    if added or removed:
        status = "DRIFTING"

    hidden_added = [
        edge for edge in edges
        if (edge.get("from"), edge.get("to")) in added
        and edge.get("hidden") is True
    ]

    effect_added = [
        edge for edge in edges
        if (edge.get("from"), edge.get("to")) in added
        and edge.get("effect_capable") is True
    ]

    if hidden_added or effect_added:
        status = "SHADOW"

    events.append({
        "timestamp": timestamp,
        "added_edges": list(added),
        "removed_edges": list(removed),
        "hidden_added_count": len(hidden_added),
        "effect_added_count": len(effect_added)
    })

    previous_edges = current_edges

report = {
    "lens": "TOPOLOGY_DRIFT_TIMELINE",
    "status": status,
    "snapshot_count": len(snapshots),
    "events": events,
    "observer_mode": True,
    "non_claims": [
        "Not runtime enforcement",
        "Not topology proof",
        "Not execution authorization",
        "Not production monitoring"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")