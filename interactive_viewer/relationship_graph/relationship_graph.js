const relationshipGraphNodes = [
  {
    id: "hospital_continuity",
    label: "Hospital",
    domain: "healthcare"
  },
  {
    id: "distributed_hospital_continuity",
    label: "Distributed Hospital",
    domain: "healthcare"
  },
  {
    id: "cyber_recoverability",
    label: "Cyber",
    domain: "cyber"
  },
  {
    id: "ai_oversight_continuity",
    label: "AI Oversight",
    domain: "ai_oversight"
  },
  {
    id: "energy_grid_recoverability",
    label: "Energy Grid",
    domain: "energy"
  },
  {
    id: "emergency_response_continuity",
    label: "Emergency",
    domain: "emergency"
  },
  {
    id: "regional_supply_chain",
    label: "Supply Chain",
    domain: "supply_chain"
  },
  {
    id: "centralized_vs_distributed_healthcare",
    label: "Healthcare Comparison",
    domain: "comparison"
  }
];

const relationshipGraphEdges = [
  {
    source: "hospital_continuity",
    target: "distributed_hospital_continuity",
    relationship: "shared healthcare continuity surface"
  },
  {
    source: "hospital_continuity",
    target: "emergency_response_continuity",
    relationship: "hospital intake / response dependency visibility"
  },
  {
    source: "distributed_hospital_continuity",
    target: "centralized_vs_distributed_healthcare",
    relationship: "centralized vs distributed topology comparison"
  },
  {
    source: "cyber_recoverability",
    target: "ai_oversight_continuity",
    relationship: "identity / audit / dependency opacity overlap"
  },
  {
    source: "cyber_recoverability",
    target: "energy_grid_recoverability",
    relationship: "control dependency and recovery corridor overlap"
  },
  {
    source: "energy_grid_recoverability",
    target: "emergency_response_continuity",
    relationship: "infrastructure dependency and response continuity overlap"
  },
  {
    source: "regional_supply_chain",
    target: "energy_grid_recoverability",
    relationship: "logistics / fuel / replacement dependency overlap"
  },
  {
    source: "regional_supply_chain",
    target: "emergency_response_continuity",
    relationship: "mobility, fuel, routing, and fallback corridor overlap"
  }
];

function renderRelationshipGraphSvg() {
  const width = 1200;
  const height = 820;
  const centerX = width / 2;
  const centerY = height / 2 + 20;
  const radius = 270;

  const positions = {};

  relationshipGraphNodes.forEach((node, index) => {
    const angle =
      -Math.PI / 2 +
      (2 * Math.PI * index) / relationshipGraphNodes.length;

    positions[node.id] = {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle)
    };
  });

  function domainColor(domain) {
    const colors = {
      healthcare: "#22c55e",
      cyber: "#8b5cf6",
      ai_oversight: "#0ea5e9",
      energy: "#f97316",
      emergency: "#ef4444",
      supply_chain: "#eab308",
      comparison: "#64748b"
    };

    return colors[domain] || "#94a3b8";
  }

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
    <text x="${centerX}" y="48" text-anchor="middle"
      font-family="Inter, Arial" font-size="26" font-weight="800"
      fill="#0f172a">
      Observatory Relationship Graph
    </text>
  `);

  parts.push(`
    <text x="${centerX}" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only topology-of-topologies continuity relationship visibility
    </text>
  `);

  relationshipGraphEdges.forEach((edge) => {
    const source = positions[edge.source];
    const target = positions[edge.target];

    if (!source || !target) {
      return;
    }

    parts.push(`
      <line
        x1="${source.x.toFixed(1)}"
        y1="${source.y.toFixed(1)}"
        x2="${target.x.toFixed(1)}"
        y2="${target.y.toFixed(1)}"
        stroke="#64748b"
        stroke-width="3"
        opacity="0.32">
        <title>${escapeText(edge.relationship)}</title>
      </line>
    `);
  });

  relationshipGraphNodes.forEach((node) => {
    const position = positions[node.id];
    const color = domainColor(node.domain);

    parts.push(`
      <g>
        <title>${escapeText(node.label + " — " + node.domain)}</title>

        <circle
          cx="${position.x.toFixed(1)}"
          cy="${position.y.toFixed(1)}"
          r="58"
          fill="${color}"
          opacity="0.18"
          stroke="${color}"
          stroke-width="3" />

        <text
          x="${position.x.toFixed(1)}"
          y="${(position.y - 4).toFixed(1)}"
          text-anchor="middle"
          font-family="Inter, Arial"
          font-size="14"
          font-weight="800"
          fill="#0f172a">
          ${escapeText(node.label)}
        </text>

        <text
          x="${position.x.toFixed(1)}"
          y="${(position.y + 17).toFixed(1)}"
          text-anchor="middle"
          font-family="Inter, Arial"
          font-size="11"
          fill="#475569">
          ${escapeText(node.domain.replaceAll("_", " "))}
        </text>
      </g>
    `);
  });

  parts.push(`
    <rect x="350" y="710" width="500" height="54" rx="16"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${centerX}" y="734" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      NON-CLAIM: Relationship graph does not score, rank, predict, govern, or certify scenarios.
    </text>

    <text x="${centerX}" y="754" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      It provides bounded cross-domain continuity relationship visibility only.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadRelationshipGraph() {
  if (!svgFrame) {
    return;
  }

  const svg = renderRelationshipGraphSvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  const url = URL.createObjectURL(blob);

  svgFrame.src = url;

  if (notesBox) {
    notesBox.textContent =
      "Observatory Relationship Graph\n\n" +
      "This graph shows scenario-to-scenario relationship visibility across shared continuity pressure surfaces.\n\n" +
      "It is observer-only and does not rank, score, predict, govern, certify, or authorize any scenario.";
  }

  resetZoom();
}