import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.visibility_extinction_boundary import (
    extract_visibility_extinction_boundary
)

INPUT_FILE = (
    ROOT / "input" /
    "sample_visibility_extinction_boundary.json"
)

OUTPUT_DIR = ROOT / "output"

SVG_FILE = (
    OUTPUT_DIR /
    "visibility_extinction_boundary.svg"
)

REPORT_FILE = (
    OUTPUT_DIR /
    "visibility_extinction_boundary_report.json"
)

RECEIPT_FILE = (
    OUTPUT_DIR /
    "visibility_extinction_boundary_receipt.json"
)


def build_svg(title, report):

    boundary = report[
        "visibility_extinction_boundary"
    ]

    return f"""
<svg xmlns="http://www.w3.org/2000/svg"
width="1900"
height="1200">

<rect width="100%" height="100%"
fill="#0d1117"/>

<text x="30" y="50"
fill="white"
font-size="34">
{title}
</text>

<text x="30" y="90"
fill="#aaaaaa"
font-size="14">
Observer-only visibility extinction boundary extraction
</text>

<circle cx="950"
cy="650"
r="280"
fill="#88ffbb"
fill-opacity="0.015"/>

<circle cx="950"
cy="650"
r="180"
fill="#88ffbb"
fill-opacity="0.025"/>

<circle cx="950"
cy="650"
r="100"
fill="#88ffbb"
fill-opacity="0.05"
stroke="#88ffbb"
stroke-opacity="0.40"
stroke-width="3"/>

<text x="950"
y="640"
text-anchor="middle"
fill="#88ffbb"
font-size="24">
Visibility Extinction Boundary
</text>

<text x="950"
y="675"
text-anchor="middle"
fill="#cccccc"
font-size="12">
visibility exhaustion boundary
</text>

<text x="950"
y="735"
text-anchor="middle"
fill="white"
font-size="14">
remaining_structure={boundary["remaining_structure"]}
</text>

<text x="950"
y="760"
text-anchor="middle"
fill="white"
font-size="14">
visibility_remainder={boundary["visibility_remainder"]}
</text>

<text x="950"
y="785"
text-anchor="middle"
fill="white"
font-size="14">
distance_to_extinction={boundary["distance_to_extinction"]}
</text>

<text x="30"
y="1120"
fill="#bbbbbb"
font-size="14">
Visibility Extinction Boundary = reduction exhaustion visibility
</text>

<text x="30"
y="1160"
fill="#888888"
font-size="12">
Historical visibility boundaries only • No prediction • UNKNOWN → HOLD
</text>

</svg>
"""


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_visibility_extinction_boundary(
        data
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title"),
        report
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "classification":
            "VISIBILITY_EXTINCTION_BOUNDARY",

        "observer_mode": True,
        "prediction": False,
        "routing": False,

        "sha256":
            hashlib.sha256(
                svg.encode()
            ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(
        "Visibility Extinction Boundary Observatory Complete"
    )


if __name__ == "__main__":
    main()