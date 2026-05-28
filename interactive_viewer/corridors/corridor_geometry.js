const corridorGeometryGroups = [
  {
    id: "fallback_corridor",
    label: "Fallback Corridor",
    description:
      "Visibility of alternate paths, backup routes, or recovery surfaces that may preserve recoverability under continuity pressure.",
    scenarios: [
      "cyber_recoverability",
      "energy_grid_recoverability",
      "emergency_response_continuity",
      "distributed_hospital_continuity"
    ]
  },
  {
    id: "oversight_corridor",
    label: "Oversight Corridor",
    description:
      "Visibility of human review, operator intervention, audit traceability, and localization surfaces under continuation pressure.",
    scenarios: [
      "ai_oversight_continuity",
      "hospital_continuity",
      "emergency_response_continuity"
    ]
  },
  {
    id: "dependency_corridor",
    label: "Dependency Corridor",
    description:
      "Visibility of concentrated or external dependency pathways where hidden coupling can preserve continuity appearance while narrowing recoverability.",
    scenarios: [
      "cyber_recoverability",
      "regional_supply_chain",
      "energy_grid_recoverability"
    ]
  }
];

function renderCorridorGeometrySvg() {
  const width = 1200;
  const height = 820;
  const cx = width / 2;

  const corridorRows = [
    {
      y: 210,
      label: "Fallback Corridor",
      left: "available",
      center: "narrowing",
      right: "constrained",
      color: "#22c55e"
    },
    {
      y: 360,
      label: "Oversight Corridor",
      left: "visible",
      center: "partial",
      right: "degraded",
      color: "#0ea5e9"
    },
    {
      y: 510,
      label: "Dependency Corridor",
      left: "distributed",
      center: "concentrated",
      right: "fragile",
      color: "#f97316"
    }
  ];

  function escapeText(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  const parts = [];

  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`
  );

  parts.push(`<rect width="${width}" height="${height}" fill="#f8fafc" />`);

  parts.push(`
    <text x="${cx}" y="48" text-anchor="middle"
      font-family="Inter, Arial" font-size="26" font-weight="800"
      fill="#0f172a">
      Continuity Corridor Geometry
    </text>
  `);

  parts.push(`
    <text x="${cx}" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only corridor contraction and recoverability pathway visibility
    </text>
  `);

  corridorRows.forEach((row) => {
    parts.push(`
      <rect x="120" y="${row.y - 58}" width="960" height="112" rx="22"
        fill="#ffffff" stroke="#cbd5e1" />

      <text x="170" y="${row.y - 18}" text-anchor="start"
        font-family="Inter, Arial" font-size="17" font-weight="800"
        fill="#0f172a">
        ${escapeText(row.label)}
      </text>

      <line x1="370" y1="${row.y}" x2="850" y2="${row.y}"
        stroke="${row.color}" stroke-width="8" opacity="0.22"
        stroke-linecap="round" />

      <circle cx="370" cy="${row.y}" r="24"
        fill="${row.color}" opacity="0.20" stroke="${row.color}" stroke-width="3" />

      <circle cx="610" cy="${row.y}" r="18"
        fill="${row.color}" opacity="0.18" stroke="${row.color}" stroke-width="3" />

      <circle cx="850" cy="${row.y}" r="12"
        fill="${row.color}" opacity="0.16" stroke="${row.color}" stroke-width="3" />

      <text x="370" y="${row.y + 48}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" fill="#475569">
        ${escapeText(row.left)}
      </text>

      <text x="610" y="${row.y + 48}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" fill="#475569">
        ${escapeText(row.center)}
      </text>

      <text x="850" y="${row.y + 48}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" fill="#475569">
        ${escapeText(row.right)}
      </text>
    `);
  });

  parts.push(`
    <rect x="260" y="690" width="680" height="64" rx="18"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${cx}" y="716" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      NON-CLAIM: Corridor geometry does not predict, score, govern, authorize, or certify recoverability.
    </text>

    <text x="${cx}" y="738" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      It provides bounded observer-only visibility into recoverability pathway contraction.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadCorridorGeometry() {
  if (!svgFrame) {
    return;
  }

  const svg = renderCorridorGeometrySvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  svgFrame.src = URL.createObjectURL(blob);

  if (notesBox) {
    notesBox.textContent =
      "Continuity Corridor Geometry\n\n" +
      "This view shows observer-only continuity corridor contraction surfaces:\n\n" +
      "• fallback corridor visibility\n" +
      "• oversight corridor visibility\n" +
      "• dependency corridor concentration\n\n" +
      "This geometry does not predict, score, govern, authorize, or certify recovery.";
  }

  resetZoom();
}