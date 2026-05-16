import json
import os

CASES_DIR = "harness/cases/present_state_dependence_cases"

print("Present-State Dependence Check")
print("--------------------------------")

for filename in sorted(os.listdir(CASES_DIR)):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(CASES_DIR, filename)

    with open(path, "r") as f:
        case = json.load(f)

    print()
    print(filename)
    print(json.dumps(case, indent=2))

    if (
        case.get("topology_visibility") in ["narrowing", "partial"]
        or case.get("dependency_visibility") == "degrading"
        or case.get("present_state_dependence") in ["uncertain", "thinning"]
        or case.get("present_state_grounding") == "unclear"
    ):
        result = "HOLD"
    else:
        result = "PASS"

    print("Suggested classification:", result)

print()
print("--------------------------------")
print("Reduction:")
print("continuity preserved != present-state dependence preserved")