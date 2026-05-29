import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.reduction_residue import (
    extract_reduction_residue
)

INPUT_FILE = (
    ROOT / "input" /
    "sample_reduction_residue.json"
)

OUTPUT_DIR = ROOT / "output"

SVG_FILE = (
    OUTPUT_DIR /
    "reduction_residue_observatory.svg"
)

REPORT_FILE = (
    OUTPUT_DIR /
    "reduction_residue_report.json"
)

RECEIPT_FILE = (
    OUTPUT_DIR /
    "reduction_residue_receipt.json"
)


def build_svg(title, report):

    residue = report["reduction_residue"]

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
Observer-only reduction residue extraction
</text>

<circle cx="950"
cy="650"
r="90"
fill="#88ffbb"
fill-opacity="0.08"
stroke="#88ffbb"
stroke-width="3"
stroke-opacity="0.45"/>

<text x="950"
y="640"
text-anchor="middle"
fill="#88ffbb"
font-size="24">
Reduction Residue
</text>

<text x="950"
y="675"
text-anchor="middle"
fill="#cccccc"
font-size="12">
irreducible structure
</text>

<text x="950"
y="735"
text-anchor="middle"
fill="white"
font-size="14">
irreducible_structure={residue["irreducible_structure"]}
</text>

<text x="950"
y="760"
text-anchor="middle"
fill="white"
font-size="14">
residue_strength={residue["residue_strength"]}
</text>

<text x="950"
y="785"
text-anchor="middle"
fill="white"
font-size="14">
reduction_depth={residue["reduction_depth"]}
</text>

<text x="30"
y="1120"
fill="#bbbbbb"
font-size="14">
Reduction Residue = irreducible observer-visible structure
</text>

<text x="30"
y="1160"
fill="#888888"
font-size="12">
Historical residue only • No prediction • UNKNOWN → HOLD
</text>

</svg>
"""


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_reduction_residue(data)

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
            "REDUCTION_RESIDUE",
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

    print("Reduction Residue Observatory Complete")


if __name__ == "__main__":
    main()