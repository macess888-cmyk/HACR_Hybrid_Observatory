from __future__ import annotations

import copy
import hashlib
import json
import math
from datetime import datetime, timezone
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

BASE_CASE = (
    ROOT
    / "scenarios"
    / "cyber_recoverability"
    / "json"
    / "cyber_recoverability_case_v1.json"
)

FRAME_DIR = ROOT / "tools" / "continuity_replay_engine" / "frames"
OUTPUT_DIR = ROOT / "tools" / "continuity_replay_engine" / "output"


REPLAY_FRAMES = [
    {
        "frame_id": "frame_001_baseline_visibility",
        "description": "Baseline cyber recoverability topology visibility.",
        "node_states": {
            "Identity": "strained",
            "EndpointFleet": "degraded",
            "BackupVault": "operational",
            "SOC": "partial",
            "NetworkCore": "operational",
            "CloudApps": "strained"
        },
        "continuity_pressure": {
            "identity_dependency": 0.86,
            "endpoint_degradation": 0.78,
            "restore_path_visibility": 0.51
        },
        "recoverability_state": {
            "interruptibility": "constrained",
            "localization_visibility": "partial",
            "recovery_corridor": "available but narrow"
        }
    },
    {
        "frame_id": "frame_002_endpoint_pressure_increase",
        "description": "Endpoint degradation increases while identity dependency remains high.",
        "node_states": {
            "Identity": "strained",
            "EndpointFleet": "degraded",
            "BackupVault": "operational",
            "SOC": "partial",
            "NetworkCore": "operational",
            "CloudApps": "strained"
        },
        "continuity_pressure": {
            "identity_dependency": 0.89,
            "endpoint_degradation": 0.91,
            "restore_path_visibility": 0.43
        },
        "recoverability_state": {
            "interruptibility": "narrowing",
            "localization_visibility": "partial",
            "recovery_corridor": "narrowing"
        }
    },
    {
        "frame_id": "frame_003_recovery_path_visibility_loss",
        "description": "Restore-path visibility narrows while continuity still appears operational.",
        "node_states": {
            "Identity": "strained",
            "EndpointFleet": "degraded",
            "BackupVault": "strained",
            "SOC": "partial",
            "NetworkCore": "operational",
            "CloudApps": "strained"
        },
        "continuity_pressure": {
            "identity_dependency": 0.91,
            "endpoint_degradation": 0.92,
            "restore_path_visibility": 0.29
        },
        "recoverability_state": {
            "interruptibility": "constrained",
            "localization_visibility": "degraded",
            "recovery_corridor": "fragile"
        }
    },
    {
        "frame_id": "frame_004_backup_recoverability_reassertion",
        "description": "Backup recoverability partially reasserts visibility without authorizing recovery.",
        "node_states": {
            "Identity": "strained",
            "EndpointFleet": "degraded",
            "BackupVault": "operational",
            "SOC": "partial",
            "NetworkCore": "operational",
            "CloudApps": "partial"
        },
        "continuity_pressure": {
            "identity_dependency": 0.84,
            "endpoint_degradation": 0.82,
            "restore_path_visibility": 0.61
        },
        "recoverability_state": {
            "interruptibility": "partially preserved",
            "localization_visibility": "partial",
            "recovery_corridor": "visible but constrained"
        }
    }
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


def state_color(state: str) -> str:
    state = str(state).lower()

    if "degraded" in state or "degrading" in state:
        return "#ef4444"

    if "strained" in state or "constrained" in state or "narrowing" in state:
        return "#f97316"

    if "partial" in state:
        return "#eab308"

    if "operational" in state:
        return "#22c55e"

    return "#94a3b8"


def apply_frame(base_case: dict, frame: dict) -> dict:
    case = copy.deepcopy(base_case)

    case["scenario_id"] = frame["frame_id"]
    case["scenario_type"] = "continuity_replay_frame"
    case["replay_frame"] = True
    case["replay_description"] = frame["description"]

    node_states = frame["node_states"]

    for node in case.get("nodes", []):
        node_id = node.get("id")

        if node_id in node_states:
            node["state"] = node_states[node_id]

    case["continuity_pressure"] = frame["continuity_pressure"]
    case["recoverability_state"] = frame["recoverability_state"]

    case["non_claims"] = {
        "not_predictive": True,
        "not_simulation_authority": True,
        "not_operational_guidance": True,
        "observer_only": True
    }

    return case


def build_replay_frames() -> list[Path]:
    base_case = load_json(BASE_CASE)
    frame_paths = []

    for frame in REPLAY_FRAMES:
        frame_case = apply_frame(base_case, frame)
        output_path = FRAME_DIR / f"{frame['frame_id']}.json"

        write_json(output_path, frame_case)
        frame_paths.append(output_path)

    return frame_paths


def build_simple_frame_svg(data: dict) -> str:
    width = 1200
    height = 820
    cx = width / 2
    cy = height / 2 + 20
    radius = 245

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    positions = {}

    for index, node in enumerate(nodes):
        angle = -math.pi / 2 + (2 * math.pi * index / max(len(nodes), 1))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions[node["id"]] = (x, y)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1200" height="820" fill="#f8fafc" />',
        f'<text x="{cx}" y="46" text-anchor="middle" font-family="Inter, Arial" font-size="25" font-weight="800" fill="#0f172a">Continuity Replay Frame</text>',
        f'<text x="{cx}" y="76" text-anchor="middle" font-family="Inter, Arial" font-size="14" fill="#475569">{escape(data.get("replay_description", "observer-only replay frame"))}</text>',
    ]

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        if source in positions and target in positions:
            x1, y1 = positions[source]
            x2, y2 = positions[target]

            parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="#64748b" stroke-width="3" opacity="0.34" />'
            )

    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in positions.values())

    parts.append(
        f'<polygon points="{points}" fill="#22c55e" fill-opacity="0.05" '
        f'stroke="#22c55e" stroke-width="5" stroke-dasharray="10,7" opacity="0.18" />'
    )

    for node in nodes:
        node_id = node.get("id")
        node_type = node.get("type", "node")
        state = node.get("state", "unknown")

        x, y = positions[node_id]
        color = state_color(state)

        parts.extend([
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="54" fill="{color}" opacity="0.18" stroke="{color}" stroke-width="3" />',
            f'<text x="{x:.1f}" y="{y - 6:.1f}" text-anchor="middle" font-family="Inter, Arial" font-size="15" font-weight="800" fill="#0f172a">{escape(node_id)}</text>',
            f'<text x="{x:.1f}" y="{y + 14:.1f}" text-anchor="middle" font-family="Inter, Arial" font-size="11" fill="#475569">{escape(node_type.replace("_", " "))}</text>',
            f'<text x="{x:.1f}" y="{y + 30:.1f}" text-anchor="middle" font-family="Inter, Arial" font-size="11" fill="#475569">{escape(state)}</text>',
        ])

    pressure = data.get("continuity_pressure", {})
    panel_y = 105
    row_y = 170

    parts.extend([
        f'<rect x="40" y="{panel_y}" width="320" height="175" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        '<text x="200" y="138" text-anchor="middle" font-family="Inter, Arial" font-size="17" font-weight="800" fill="#0f172a">Replay Pressure</text>',
    ])

    for key, value in pressure.items():
        bar = max(0, min(1, float(value))) * 130

        parts.extend([
            f'<text x="65" y="{row_y}" text-anchor="start" font-family="Inter, Arial" font-size="11" fill="#475569">{escape(key.replace("_", " "))}</text>',
            f'<rect x="210" y="{row_y - 10}" width="130" height="10" rx="5" fill="#e2e8f0" />',
            f'<rect x="210" y="{row_y - 10}" width="{bar:.1f}" height="10" rx="5" fill="#64748b" />',
        ])

        row_y += 34

    recoverability = data.get("recoverability_state", {})

    parts.extend([
        '<rect x="840" y="105" width="320" height="175" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        '<text x="1000" y="138" text-anchor="middle" font-family="Inter, Arial" font-size="17" font-weight="800" fill="#0f172a">Recoverability State</text>',
    ])

    recovery_y = 170

    for key, value in recoverability.items():
        parts.append(
            f'<text x="870" y="{recovery_y}" text-anchor="start" font-family="Inter, Arial" font-size="12" fill="#475569">{escape(key.replace("_", " "))}: {escape(str(value))}</text>'
        )
        recovery_y += 28

    parts.extend([
        f'<text x="{cx}" y="{height - 42}" text-anchor="middle" font-family="Inter, Arial" font-size="13" font-weight="800" fill="#475569">NON-CLAIM: Replay frames do not predict, govern, authorize, certify, or replace operators.</text>',
        f'<text x="{cx}" y="{height - 20}" text-anchor="middle" font-family="Inter, Arial" font-size="13" fill="#475569">Continuity replay is bounded observer-only topology evolution visibility.</text>',
        "</svg>",
    ])

    return "\n".join(parts)


def render_frames(frame_paths: list[Path]) -> None:
    for frame_path in frame_paths:
        data = load_json(frame_path)
        svg = build_simple_frame_svg(data)

        output_svg = OUTPUT_DIR / f"{frame_path.stem}.svg"

        output_svg.parent.mkdir(parents=True, exist_ok=True)
        output_svg.write_text(svg, encoding="utf-8")


def write_replay_receipt(frame_paths: list[Path]) -> None:
    frames = []

    for frame_path in frame_paths:
        svg_path = OUTPUT_DIR / f"{frame_path.stem}.svg"

        frame_text = frame_path.read_text(encoding="utf-8")
        svg_text = svg_path.read_text(encoding="utf-8")

        frames.append({
            "frame_json": str(frame_path.relative_to(ROOT)),
            "frame_svg": str(svg_path.relative_to(ROOT)),
            "frame_json_sha256": sha256_text(frame_text),
            "frame_svg_sha256": sha256_text(svg_text),
        })

    receipt = {
        "replay_id": "cyber_recoverability_continuity_replay_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_case": str(BASE_CASE.relative_to(ROOT)),
        "observer_only": True,
        "non_authoritative": True,
        "frame_count": len(frames),
        "frames": frames,
        "non_claims": {
            "not_predictive": True,
            "not_simulation_authority": True,
            "not_operational_guidance": True,
            "not_certification": True
        }
    }

    write_json(
        OUTPUT_DIR / "cyber_recoverability_replay_receipt.json",
        receipt
    )


def main() -> None:
    frame_paths = build_replay_frames()
    render_frames(frame_paths)
    write_replay_receipt(frame_paths)

    print("Continuity replay frames generated:")

    for frame_path in frame_paths:
        print(f"- {frame_path}")

    print(f"Receipt: {OUTPUT_DIR / 'cyber_recoverability_replay_receipt.json'}")


if __name__ == "__main__":
    main()