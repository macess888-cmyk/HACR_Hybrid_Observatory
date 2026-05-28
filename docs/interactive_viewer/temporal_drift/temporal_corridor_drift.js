const temporalCorridorFrames = [
  {
    label: "t1 — Baseline Visibility",
    fallback: 0.72,
    oversight: 0.66,
    dependency: 0.58,
    note: "Corridors remain visible, but dependency concentration is already present."
  },
  {
    label: "t2 — Pressure Increase",
    fallback: 0.54,
    oversight: 0.49,
    dependency: 0.72,
    note: "Fallback and oversight visibility narrow while dependency pressure increases."
  },
  {
    label: "t3 — Recoverability Contraction",
    fallback: 0.31,
    oversight: 0.34,
    dependency: 0.86,
    note: "Recoverability corridors contract under concentrated dependency pressure."
  },
  {
    label: "t4 — Partial Reassertion",
    fallback: 0.59,
    oversight: 0.47,
    dependency: 0.64,
    note: "Fallback visibility partially reasserts, but oversight remains constrained."
  }
];

let temporalDriftIndex = 0;

function currentTemporalFrame() {
  return temporalCorridorFrames[temporalDriftIndex];
}

function renderTemporalCorridorDriftSvg() {
  const width = 1200;
  const height = 820;
  const frame = currentTemporalFrame();

  function xFromValue(value) {
    return 260 + value * 620;
  }

  function row(y, label, value, color, leftLabel, rightLabel) {
    const x = xFromValue(value);

    return `
      <rect x="120" y="${y - 56}" width="960" height="112" rx="22"
        fill="#ffffff" stroke="#cbd5e1" />

      <text x="170" y="${y - 20}" text-anchor="start"
        font-family="Inter, Arial" font-size="17" font-weight="800"
        fill="#0f172a">
        ${label}
      </text>

      <line x1="260" y1="${y}" x2="880" y2="${y}"
        stroke="${color}" stroke-width="8" opacity="0.18"
        stroke-linecap="round" />

      <circle cx="${x}" cy="${y}" r="25"
        fill="${color}" opacity="0.24" stroke="${color}" stroke-width="3" />

      <text x="260" y="${y + 44}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" fill="#475569">
        ${leftLabel}
      </text>

      <text x="880" y="${y + 44}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" fill="#475569">
        ${rightLabel}
      </text>

      <text x="${x}" y="${y - 34}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" font-weight="700"
        fill="#475569">
        ${Math.round(value * 100)}%
      </text>
    `;
  }

  const parts = [];

  parts.push(`
    <svg xmlns="http://www.w3.org/2000/svg"
      width="${width}" height="${height}"
      viewBox="0 0 ${width} ${height}">
  `);

  parts.push(`<rect width="${width}" height="${height}" fill="#f8fafc" />`);

  parts.push(`
    <text x="600" y="48" text-anchor="middle"
      font-family="Inter, Arial" font-size="26" font-weight="800"
      fill="#0f172a">
      Temporal Corridor Drift
    </text>

    <text x="600" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only corridor movement across bounded replay frames
    </text>

    <text x="600" y="118" text-anchor="middle"
      font-family="Inter, Arial" font-size="18" font-weight="800"
      fill="#0f172a">
      ${frame.label}
    </text>

    <text x="600" y="146" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      ${frame.note}
    </text>
  `);

  parts.push(
    row(
      250,
      "Fallback Corridor Visibility",
      frame.fallback,
      "#22c55e",
      "contracted",
      "available"
    )
  );

  parts.push(
    row(
      400,
      "Oversight Corridor Visibility",
      frame.oversight,
      "#0ea5e9",
      "degraded",
      "visible"
    )
  );

  parts.push(
    row(
      550,
      "Dependency Pressure",
      frame.dependency,
      "#f97316",
      "distributed",
      "concentrated"
    )
  );

  parts.push(`
    <rect x="250" y="690" width="700" height="64" rx="18"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="600" y="716" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      NON-CLAIM: Temporal drift does not predict, score, govern, authorize, or certify recoverability.
    </text>

    <text x="600" y="738" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      It shows bounded observer-only corridor movement visibility.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadTemporalCorridorDrift() {
  if (!svgFrame) {
    return;
  }

  const svg = renderTemporalCorridorDriftSvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  svgFrame.src = URL.createObjectURL(blob);

  if (notesBox) {
    const frame = currentTemporalFrame();

    notesBox.textContent =
      "Temporal Corridor Drift\n\n" +
      frame.label +
      "\n\n" +
      frame.note +
      "\n\nFallback corridor: " +
      Math.round(frame.fallback * 100) +
      "%\nOversight corridor: " +
      Math.round(frame.oversight * 100) +
      "%\nDependency pressure: " +
      Math.round(frame.dependency * 100) +
      "%\n\nThis view remains observer-only and non-authoritative.";
  }

  resetZoom();
}

function nextTemporalDriftFrame() {
  temporalDriftIndex = Math.min(
    temporalDriftIndex + 1,
    temporalCorridorFrames.length - 1
  );

  loadTemporalCorridorDrift();
}

function previousTemporalDriftFrame() {
  temporalDriftIndex = Math.max(
    temporalDriftIndex - 1,
    0
  );

  loadTemporalCorridorDrift();
}

function firstTemporalDriftFrame() {
  temporalDriftIndex = 0;
  loadTemporalCorridorDrift();
}

function lastTemporalDriftFrame() {
  temporalDriftIndex = temporalCorridorFrames.length - 1;
  loadTemporalCorridorDrift();
}