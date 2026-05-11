import json
import os

INPUT_FILE = "Inputs/language_simplifier_case.json"
OUTPUT_FILE = "Outputs/language_simplifier_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

term = data.get("term", "")
technical = data.get("technical", "")

plain_map = {
    "SHADOW": "Something hidden or indirect may still be reachable.",
    "HOLD": "There is not enough clear information to safely classify this.",
    "FAIL": "The tested condition breaks the expected boundary.",
    "PASS": "The tested condition appears bounded in this input.",
    "bind freshness": "The system must check the condition again at the moment of action.",
    "topology": "The map of paths a system can still use.",
    "reachability": "Whether a path can still get to an effect.",
    "observer-restricted": "This tool only inspects and reports. It does not approve or control anything."
}

plain = plain_map.get(term, "This term needs narrowing before it is safe to explain publicly.")

report = {
    "term": term,
    "technical_input": technical,
    "plain_language": plain,
    "child_safe": plain,
    "executive_summary": plain,
    "observer_mode": True,
    "non_claims": [
        "Not authority",
        "Not certification",
        "Not legal advice",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> LANGUAGE_SIMPLIFIED")