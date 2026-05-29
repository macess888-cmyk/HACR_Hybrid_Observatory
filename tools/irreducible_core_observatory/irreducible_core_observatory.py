import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.irreducible_core import (
    extract_irreducible_core
)

INPUT_FILE = ROOT / "input" / "sample_irreducible_core.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "irreducible_core_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "irreducible_core_report.json"
RECEIPT_FILE = OUTPUT_DIR / "irreducible_core_receipt.json"


def build_svg(title, report):
    core = report["irreducible_core"]

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1900" height="1200">

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="30" y="50" fill="white" font-size="34">
{title}
</text>

<text x="30" y="90" fill="#aaaaaa" font-size="14">
Observer-only irreducible core extraction
</text>

<circle cx="950" cy="650"
r="72"
fill="#88ffbb"
fill-opacity="0.10"
stroke="#88ffbb"
stroke-width="4"
stroke-opacity="0.50"/>

<text x="950" y="640"
text-anchor="middle"
fill="#88ffbb"
font-size="24">
Irreducible Core
</text>

<text x="950" y="675"
text-anchor="middle"
fill="#cccccc"
font-size="12">
deepest reduction-stable residue
</text>

<text x="950" y="735"
text-anchor="middle"
fill="white"
font-size="14">
core_structure={core["core_structure"]}
</text>

<text x="950" y="760"
text-anchor="middle"
fill="white"
font-size="14">
core_stability={core["core_stability"]}
</text>

<text x="950" y="785"
text-anchor="middle"
fill="white"
font-size="14">
reduction_limit={core["reduction_limit"]}
</text>

<text x="30" y="1120"
fill="#bbbbbb"
font-size="14">
Irreducible Core = deepest observer-visible reduction-stable artifact
</text>

<text x="30" y="1160"
fill="#888888"
font-size="12">
Historical core only • No prediction • UNKNOWN → HOLD
</text>

</svg>
"""


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_irreducible_core(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(data.get("title"), report)

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "classification": "IRREDUCIBLE_CORE",
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "sha256": hashlib.sha256(svg.encode()).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Irreducible Core Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()