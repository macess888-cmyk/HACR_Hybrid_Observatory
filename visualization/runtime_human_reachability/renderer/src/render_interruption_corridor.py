import argparse
import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path


STATUS_STYLES = {
    "PASS": {
        "stroke": "#2f855a",
        "dash": "0",
        "label": "PASS"
    },
    "HOLD": {
        "stroke": "#b7791f",
        "dash": "6 4",
        "label": "HOLD"
    },
    "FAIL": {
        "stroke": "#c53030",
        "dash": "2 3",
        "label": "FAIL"
    }
}


NON_CLAIMS = [
    "does not govern",
    "does not authorize",
    "does not certify",
    "does not determine legitimacy",
    "does not infer inevitability",
    "does not operationalize consequence",
    "does not replace bind proof"
]


def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_svg(case):
    nodes = {node["id"]: node for node in case.get("nodes", [])}
    edges = case.get("edges", [])

    width = 760
    height = 260

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append('<rect width="100%" height="100%" fill="white"/>')
    parts.append('<text x="30" y="30" font-size="18" font-family="Arial" font-weight="bold">Runtime Human Reachability: Interruption Corridor Map</text>')
    parts.append('<text x="30" y="52" font-size="12" font-family="Arial">Observer-only deterministic rendering. A map is not authority. UNKNOWN -&gt; HOLD.</text>')

    for edge in edges:
        source = nodes.get(edge["from"])
        target = nodes.get(edge["to"])

        if not source or not target:
            continue

        status = edge.get("status", "HOLD")
        pressure = edge.get("pressure", "UNKNOWN")
        style = STATUS_STYLES.get(status, STATUS_STYLES["HOLD"])

        x1 = source["x"] + 55
        y1 = source["y"]
        x2 = target["x"] - 55
        y2 = target["y"]

        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{style["stroke"]}" stroke-width="4" stroke-dasharray="{style["dash"]}"/>'
        )

        mid_x = (x1 + x2) / 2
        mid_y = y1 - 14

        parts.append(
            f'<text x="{mid_x}" y="{mid_y}" font-size="11" font-family="Arial" text-anchor="middle">'
            f'{status} | pressure={pressure}</text>'
        )

    for node in case.get("nodes", []):
        x = node["x"]
        y = node["y"]
        label = node["label"]

        parts.append(f'<circle cx="{x}" cy="{y}" r="42" fill="#f7fafc" stroke="#2d3748" stroke-width="2"/>')
        parts.append(
            f'<text x="{x}" y="{y - 4}" font-size="11" font-family="Arial" text-anchor="middle">{label}</text>'
        )

    parts.append('<text x="30" y="225" font-size="11" font-family="Arial">Non-claims: does not govern | does not authorize | does not certify | does not determine legitimacy</text>')
    parts.append('<text x="30" y="242" font-size="11" font-family="Arial">Break survivability, not ontology.</text>')
    parts.append("</svg>")

    return "\n".join(parts)


def build_receipt(case, svg_text, output_svg_path):
    receipt = {
        "case_id": case.get("case_id", "UNKNOWN"),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "observer_only": True,
        "artifact_type": "runtime_human_reachability_svg",
        "output_svg": str(output_svg_path),
        "svg_sha256": sha256_text(svg_text),
        "non_claims": NON_CLAIMS,
        "verdict_semantics": {
            "PASS": "interruption corridor remains materially traversable",
            "HOLD": "conditions cannot be materially reconstructed or measured",
            "FAIL": "corridor becomes visible but practically non-traversable"
        }
    }

    receipt_text = json.dumps(receipt, indent=2, sort_keys=True)
    receipt["receipt_sha256"] = sha256_text(receipt_text)

    return receipt


def main():
    parser = argparse.ArgumentParser(
        description="Render deterministic runtime human reachability SVG maps."
    )
    parser.add_argument("--case", required=True, help="Path to corridor case JSON")
    parser.add_argument(
        "--outdir",
        default="visualization/runtime_human_reachability/renderer/outputs",
        help="Output directory"
    )

    args = parser.parse_args()

    case_path = Path(args.case)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    case = load_case(case_path)
    svg_text = render_svg(case)

    base = case.get("case_id", case_path.stem)
    svg_path = outdir / f"{base}_corridor_map.svg"
    receipt_path = outdir / f"{base}_corridor_map_receipt.json"

    svg_path.write_text(svg_text, encoding="utf-8")

    receipt = build_receipt(case, svg_text, svg_path)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")

    print("Artifacts written:")
    print(f" - {svg_path}")
    print(f" - {receipt_path}")
    print(f"SVG SHA256: {receipt['svg_sha256']}")


if __name__ == "__main__":
    main()