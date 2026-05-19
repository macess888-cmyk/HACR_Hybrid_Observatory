from pathlib import Path
import json
import re
import argparse
from datetime import datetime, UTC

ROOT = Path.cwd()
SCAN_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx"}

SETTER_PATTERN = re.compile(r"\bset[A-Z][A-Za-z0-9_]*\s*\(")
EFFECT_PATTERN = re.compile(r"\buse(?:Layout)?Effect\s*\(")
DEPENDENCY_PATTERN = re.compile(r"\[([^\]]*)\]")


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def find_js_files(root):
    ignored = {"node_modules", ".git", "dist", "build", ".next", "coverage"}

    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.suffix.lower() in SCAN_EXTENSIONS:
            yield path


def line_number(text, index):
    return text[:index].count("\n") + 1


def scan_file(path):
    text = read_text(path)
    findings = []

    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if SETTER_PATTERN.search(stripped):
            if not stripped.startswith("//"):
                if "useEffect" not in stripped and "useLayoutEffect" not in stripped:
                    findings.append({
                        "type": "possible_state_update",
                        "line": i,
                        "severity": "HOLD",
                        "message": "State setter detected. Review whether this runs during render or inside an unguarded loop.",
                        "snippet": stripped[:220]
                    })

    for match in EFFECT_PATTERN.finditer(text):
        start = match.start()
        effect_slice = text[start:start + 1200]
        effect_line = line_number(text, start)

        setters = SETTER_PATTERN.findall(effect_slice)
        deps_match = DEPENDENCY_PATTERN.search(effect_slice)

        if setters:
            finding = {
                "type": "effect_state_update",
                "line": effect_line,
                "severity": "HOLD",
                "message": "Effect contains state update. Verify dependency guard prevents repeated update loop.",
                "setters": sorted(set(s.replace("(", "").strip() for s in setters))
            }

            if deps_match:
                finding["dependencies"] = deps_match.group(1).strip()

            findings.append(finding)

    return findings


def main():
    parser = argparse.ArgumentParser(description="Detect possible React update loop patterns.")
    parser.add_argument("--root", default=".", help="Root directory to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    all_findings = []

    for path in find_js_files(root):
        findings = scan_file(path)
        if findings:
            all_findings.append({
                "path": str(path.relative_to(root)),
                "findings": findings
            })

    receipt = {
        "tool": "react_update_loop_detector",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "root": str(root),
        "files_with_findings": len(all_findings),
        "observer_only": True,
        "verdict": "HOLD" if all_findings else "PASS",
        "findings": all_findings,
        "non_claims": [
            "does not certify correctness",
            "does not prove root cause",
            "does not modify code",
            "UNKNOWN -> HOLD"
        ]
    }

    if args.json:
        print(json.dumps(receipt, indent=2))
        return

    print("React Update Loop Detector")
    print("--------------------------")
    print(f"Verdict: {receipt['verdict']}")
    print(f"Files with findings: {receipt['files_with_findings']}")
    print("--------------------------")

    for item in all_findings:
        print(item["path"])
        for finding in item["findings"]:
            print(f"  line {finding['line']}: {finding['type']} [{finding['severity']}]")
            print(f"    {finding['message']}")

    print("--------------------------")
    print("Findings are diagnostic only.")
    print("UNKNOWN -> HOLD.")


if __name__ == "__main__":
    main()