from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

PATTERNS = {
    "unsafe_innerHTML": r"\.innerHTML\s*=",
    "document_write": r"document\.write\s*\(",
    "inline_event_handler": r"on(click|load|error|mouseover|submit)\s*=",
    "script_injection": r"createElement\s*\(\s*['\"]script['\"]\s*\)",
    "unsafe_eval": r"\beval\s*\(",
    "function_constructor": r"new\s+Function\s*\(",
    "location_to_dom": r"(location\.search|location\.hash|window\.location).*",
}

SCAN_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".html", ".htm", ".vue", ".svelte"}

def scan_file(path: Path):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for name, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            line_no = text[:match.start()].count("\n") + 1
            findings.append((name, line_no))

    return findings

def main():
    print("=== XSS SURFACE EXPOSURE DETECTOR ===")
    print("Mode: defensive surface scan only")
    print()

    total = 0

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue

        findings = scan_file(path)
        if findings:
            rel = path.relative_to(ROOT)
            print(f"\n{rel}")
            for name, line_no in findings:
                print(f"  line {line_no}: {name}")
                total += 1

    print()
    print(f"Total potential exposure indicators: {total}")

    if total == 0:
        print("PASS: no obvious XSS exposure indicators detected")
    else:
        print("HOLD: review detected XSS exposure indicators manually")

    print()
    print("Detect exposure. Do not exploit.")
    print("UNKNOWN -> HOLD.")

if __name__ == "__main__":
    main()