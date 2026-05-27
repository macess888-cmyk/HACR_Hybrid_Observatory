from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FRAME_DIR = ROOT / "tools" / "continuity_replay_engine" / "frames"
OUTPUT_DIR = ROOT / "tools" / "frame_delta_overlay" / "output"

FRAME_PAIRS = [
    (
        "frame_001_baseline_visibility.json",
        "frame_002_endpoint_pressure_increase.json",
    ),
    (
        "frame_002_endpoint_pressure_increase.json",
        "frame_003_recovery_path_visibility_loss.json",
    ),
    (
        "frame_003_recovery_path_visibility_loss.json",
        "frame_004_backup_recoverability_reassertion.json",
    ),
]


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)

    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def node_state_map(frame: dict) -> dict:
    return {
        node.get("id"): node.get("state", "unknown")
        for node in frame.get("nodes", [])
    }


def pressure_delta(before: dict, after: dict) -> dict:
    before_pressure = before.get("continuity_pressure", {})
    after_pressure = after.get("continuity_pressure", {})

    keys = sorted(set(before_pressure.keys()) | set(after_pressure.keys()))

    deltas = {}

    for key in keys:
        before_value = float(before_pressure.get(key, 0))
        after_value = float(after_pressure.get(key, 0))

        deltas[key] = {
            "before": before_value,
            "after": after_value,
            "delta": round(after_value - before_value, 4),
        }

    return deltas


def state_transitions(before: dict, after: dict) -> dict:
    before_nodes = node_state_map(before)
    after_nodes = node_state_map(after)

    keys = sorted(set(before_nodes.keys()) | set(after_nodes.keys()))

    transitions = {}

    for key in keys:
        before_state = before_nodes.get(key, "missing")
        after_state = after_nodes.get(key, "missing")

        if before_state != after_state:
            transitions[key] = {
                "before": before_state,
                "after": after_state,
            }

    return transitions


def recoverability_delta(before: dict, after: dict) -> dict:
    before_state = before.get("recoverability_state", {})
    after_state = after.get("recoverability_state", {})

    keys = sorted(set(before_state.keys()) | set(after_state.keys()))

    deltas = {}

    for key in keys:
        before_value = before_state.get(key, "unknown")
        after_value = after_state.get(key, "unknown")

        if before_value != after_value:
            deltas[key] = {
                "before": before_value,
                "after": after_value,
            }

    return deltas


def build_delta(before_path: Path, after_path: Path) -> dict:
    before = load_json(before_path)
    after = load_json(after_path)

    return {
        "delta_id": f"{before_path.stem}__to__{after_path.stem}",
        "before_frame": str(before_path.relative_to(ROOT)),
        "after_frame": str(after_path.relative_to(ROOT)),
        "observer_only": True,
        "non_authoritative": True,
        "pressure_delta": pressure_delta(before, after),
        "node_state_transitions": state_transitions(before, after),
        "recoverability_delta": recoverability_delta(before, after),
        "non_claims": {
            "not_predictive": True,
            "not_scoring": True,
            "not_operational_guidance": True,
            "not_authorization": True,
            "observer_only": True,
        },
    }


def delta_summary_lines(delta: dict) -> list[str]:
    lines = []

    for key, value in delta.get("pressure_delta", {}).items():
        direction = "increased" if value["delta"] > 0 else "decreased" if value["delta"] < 0 else "unchanged"
        lines.append(
            f"{key.replace('_', ' ')} {direction}: "
            f"{value['before']:.2f} → {value['after']:.2f}"
        )

    for node_id, transition in delta.get("node_state_transitions", {}).items():
        lines.append(
            f"{node_id}: {transition['before']} → {transition['after']}"
        )

    for key, transition in delta.get("recoverability_delta", {}).items():
        lines.append(
            f"{key.replace('_', ' ')}: {transition['before']} → {transition['after']}"
        )

    return lines or ["No visible delta detected."]


def build_delta_svg(delta: dict) -> str:
    width = 1200
    height = 820

    lines = delta_summary_lines(delta)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1200" height="820" fill="#f8fafc" />',
        '<text x="600" y="48" text-anchor="middle" font-family="Inter, Arial" font-size="26" font-weight="800" fill="#0f172a">Frame Delta Overlay</text>',
        f'<text x="600" y="78" text-anchor="middle" font-family="Inter, Arial" font-size="14" fill="#475569">{escape(delta["delta_id"])}</text>',
        '<rect x="180" y="120" width="840" height="520" rx="22" fill="#ffffff" stroke="#cbd5e1" />',
        '<text x="600" y="160" text-anchor="middle" font-family="Inter, Arial" font-size="18" font-weight="800" fill="#0f172a">Observed Frame-to-Frame Changes</text>',
    ]

    y = 210

    for line in lines[:14]:
        color = "#475569"

        if "increased" in line or "degraded" in line or "narrowing" in line or "fragile" in line:
            color = "#ef4444"
        elif "decreased" in line or "reassertion" in line or "visible" in line or "preserved" in line:
            color = "#22c55e"

        parts.append(
            f'<text x="230" y="{y}" text-anchor="start" font-family="Inter, Arial" font-size="15" fill="{color}">• {escape(line)}</text>'
        )
        y += 32

    parts.extend([
        '<rect x="300" y="680" width="600" height="52" rx="16" fill="#ffffff" stroke="#cbd5e1" />',
        '<text x="600" y="712" text-anchor="middle" font-family="Inter, Arial" font-size="13" font-weight="800" fill="#475569">NON-CLAIM: Delta overlays do not score, predict, govern, authorize, or certify.</text>',
        '<text x="600" y="760" text-anchor="middle" font-family="Inter, Arial" font-size="13" fill="#475569">Observer-only bounded continuity evolution visibility.</text>',
        "</svg>",
    ])

    return "\n".join(parts)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    receipt_entries = []

    for before_name, after_name in FRAME_PAIRS:
        before_path = FRAME_DIR / before_name
        after_path = FRAME_DIR / after_name

        delta = build_delta(before_path, after_path)

        delta_json_path = OUTPUT_DIR / f"{delta['delta_id']}.json"
        delta_svg_path = OUTPUT_DIR / f"{delta['delta_id']}.svg"

        write_json(delta_json_path, delta)

        svg = build_delta_svg(delta)
        delta_svg_path.write_text(svg, encoding="utf-8")

        receipt_entries.append({
            "delta_id": delta["delta_id"],
            "delta_json": str(delta_json_path.relative_to(ROOT)),
            "delta_svg": str(delta_svg_path.relative_to(ROOT)),
            "delta_json_sha256": sha256_text(delta_json_path.read_text(encoding="utf-8")),
            "delta_svg_sha256": sha256_text(svg),
        })

    receipt = {
        "delta_overlay_receipt_id": "cyber_recoverability_frame_delta_overlay_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "observer_only": True,
        "non_authoritative": True,
        "delta_count": len(receipt_entries),
        "deltas": receipt_entries,
        "non_claims": {
            "not_predictive": True,
            "not_scoring": True,
            "not_operational_guidance": True,
            "not_authorization": True,
            "not_certification": True,
        },
    }

    write_json(
        OUTPUT_DIR / "frame_delta_overlay_receipt.json",
        receipt,
    )

    print("Frame delta overlays generated:")
    for entry in receipt_entries:
        print(f"- {entry['delta_svg']}")


if __name__ == "__main__":
    main()