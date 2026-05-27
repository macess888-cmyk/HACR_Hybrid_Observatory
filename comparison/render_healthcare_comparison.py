from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CENTRALIZED_SVG = ROOT / "scenarios" / "hospital_continuity" / "svg" / "hospital_continuity_topology.svg"
DISTRIBUTED_SVG = ROOT / "scenarios" / "distributed_hospital_continuity" / "svg" / "distributed_hospital_continuity_topology.svg"

OUTPUT_SVG = ROOT / "comparison" / "svg" / "centralized_vs_distributed_healthcare.svg"
RECEIPT = ROOT / "comparison" / "receipts" / "centralized_vs_distributed_healthcare_receipt.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_svg_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.find(">")
    end = text.rfind("</svg>")

    if start == -1 or end == -1:
        raise ValueError(f"Invalid SVG structure: {path}")

    return text[start + 1:end]


def main() -> None:
    if not CENTRALIZED_SVG.exists():
        raise FileNotFoundError(CENTRALIZED_SVG)

    if not DISTRIBUTED_SVG.exists():
        raise FileNotFoundError(DISTRIBUTED_SVG)

    centralized = read_svg_body(CENTRALIZED_SVG)
    distributed = read_svg_body(DISTRIBUTED_SVG)

    output = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="920" viewBox="0 0 2400 920">
<rect width="2400" height="920" fill="#f8fafc" />

<text x="1200" y="44" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="800" text-anchor="middle" fill="#0f172a">
Centralized vs Distributed Healthcare Continuity Comparison
</text>

<text x="1200" y="76" font-family="Inter, Arial, sans-serif" font-size="15" text-anchor="middle" fill="#475569">
Observer-only bounded deterministic comparison export
</text>

<g transform="translate(0,80) scale(0.95)">
{centralized}
</g>

<g transform="translate(1200,80) scale(0.95)">
{distributed}
</g>

<line x1="1200" y1="110" x2="1200" y2="875" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="8,8" />

<text x="1200" y="900" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="700" text-anchor="middle" fill="#475569">
NON-CLAIM: This comparison does not score, optimize, predict, authorize, certify, or replace operators.
</text>
</svg>
'''

    OUTPUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SVG.write_text(output, encoding="utf-8")

    receipt = {
        "comparison_id": "centralized_vs_distributed_healthcare",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "observer_only": True,
        "non_authoritative": True,
        "inputs": {
            "centralized_svg": str(CENTRALIZED_SVG.relative_to(ROOT)),
            "distributed_svg": str(DISTRIBUTED_SVG.relative_to(ROOT)),
        },
        "output": str(OUTPUT_SVG.relative_to(ROOT)),
        "output_sha256": sha256_text(output),
        "non_claims": {
            "not_predictive": True,
            "not_scoring": True,
            "not_optimization": True,
            "not_authorization": True,
            "not_certification": True,
            "not_operator_replacement": True,
        },
    }

    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print(f"Comparison SVG: {OUTPUT_SVG}")
    print(f"Receipt:        {RECEIPT}")


if __name__ == "__main__":
    main()