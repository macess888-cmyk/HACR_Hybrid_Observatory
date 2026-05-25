import json

RULES = [
    ("visibility", "enforcement"),
    ("continuity", "legitimacy"),
    ("replayability", "proof"),
    ("coherence", "grounding"),
    ("artifact_density", "authority")
]

sample_case = {
    "visibility": True,
    "enforcement": False,
    "continuity": True,
    "legitimacy": True,
    "replayability": True,
    "proof": False,
    "coherence": True,
    "grounding": False,
    "artifact_density": True,
    "authority": True
}

results = []

for source, target in RULES:

    if sample_case.get(source) and sample_case.get(target):
        results.append({
            "source": source,
            "target": target,
            "status": "HOLD",
            "reason": "possible false inheritance"
        })

output = {
    "inspection_result": "HOLD" if results else "PASS",
    "drift_vectors": results,
    "observer_scope": "bounded_observer_local"
}

print(json.dumps(output, indent=2))