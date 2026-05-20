import json
from pathlib import Path

INPUT = Path("sample_react_error_input.json")
OUTPUT = Path("sample_react_error_output.json")

def audit(data):
    signals = data.get("signals", {})

    if data.get("error_code") != "185":
        return {
            "decision": "HOLD",
            "likely_cause": "Unsupported or unknown React error code",
            "fix_path": [
                "Run React in development mode",
                "Collect full error message",
                "Re-run auditor with supported error signal"
            ],
            "runtime_reduction": "UNKNOWN -> HOLD"
        }

    if signals.get("set_state_in_render"):
        return {
            "decision": "FIX",
            "likely_cause": "setState called during render",
            "fix_path": [
                "Move state update out of render path",
                "Use event handler or guarded effect",
                "Re-run app"
            ],
            "runtime_reduction": "State updates must not recursively recreate their own trigger."
        }

    if signals.get("effect_updates_watched_dependency"):
        return {
            "decision": "FIX",
            "likely_cause": "useEffect updates a dependency it also watches",
            "fix_path": [
                "Inspect useEffect dependency array",
                "Find state updated inside effect",
                "Remove circular dependency or add guard",
                "Re-run app"
            ],
            "runtime_reduction": "State updates must not recursively recreate their own trigger."
        }

    if signals.get("effect_without_dependency_array_updates_state"):
        return {
            "decision": "FIX",
            "likely_cause": "useEffect without dependency array updates state repeatedly",
            "fix_path": [
                "Add dependency array",
                "Guard state update",
                "Confirm effect does not run infinitely",
                "Re-run app"
            ],
            "runtime_reduction": "Unbounded effects can recreate their own trigger."
        }

    if signals.get("unstable_dependency_identity"):
        return {
            "decision": "HOLD",
            "likely_cause": "Unstable object, array, or function dependency may retrigger effect",
            "fix_path": [
                "Inspect dependency array",
                "Stabilize identity with useMemo/useCallback only when needed",
                "Avoid creating dependency values inline when they trigger effects",
                "Re-run app"
            ],
            "runtime_reduction": "Unstable identity may camouflage update loops."
        }

    if signals.get("parent_child_recursive_update"):
        return {
            "decision": "FIX",
            "likely_cause": "Parent/child recursive update loop",
            "fix_path": [
                "Trace parent state update",
                "Trace child callback update",
                "Break recursive update path",
                "Re-run app"
            ],
            "runtime_reduction": "Recursive update paths must be broken before proceed."
        }

    return {
        "decision": "HOLD",
        "likely_cause": "No known loop pattern identified",
        "fix_path": [
            "Run non-minified React development build",
            "Inspect component stack",
            "Search recent changes for state updates",
            "Re-run auditor with updated signals"
        ],
        "runtime_reduction": "UNKNOWN -> HOLD"
    }

def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    result = audit(data)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()