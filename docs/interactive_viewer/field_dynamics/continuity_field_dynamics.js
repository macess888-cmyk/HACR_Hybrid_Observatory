const continuityFieldFrames = [
  {
    label: "Field t1 — Distributed Visibility",
    centerPressure: 0.38,
    basinIntegrity: 0.74,
    corridorElasticity: 0.69,
    note: "Continuity field remains distributed with visible recoverability basin structure."
  },
  {
    label: "Field t2 — Pressure Propagation",
    centerPressure: 0.61,
    basinIntegrity: 0.56,
    corridorElasticity: 0.47,
    note: "Pressure begins concentrating toward the field center while basin integrity narrows."
  },
  {
    label: "Field t3 — Basin Deformation",
    centerPressure: 0.82,
    basinIntegrity: 0.33,
    corridorElasticity: 0.29,
    note: "Recoverability basin visibly deforms under concentrated pressure."
  },
  {
    label: "Field t4 — Partial Basin Re-expansion",
    centerPressure: 0.52,
    basinIntegrity: 0.58,
    corridorElasticity: 0.51,
    note: "Basin visibility partially re-expands without asserting recovery success."
  }
];

let continuityFieldIndex = 0;

function currentContinuityFieldFrame() {
  return continuityFieldFrames[continuityFieldIndex];
}

function renderContinuityFieldDynamicsSvg() {
  const width = 1200;
  const height = 820;
  const cx = width / 2;
  const cy = height / 2 + 30;
  const frame = currentContinuityFieldFrame();

  const basinRadius = 120 + frame.basinIntegrity * 210;
  const pressureRadius = 40 + frame.centerPressure * 110;
  const corridorWidth = 4 + frame.corridorElasticity * 16;

  function pct(value) {
    return Math.round(value * 100);
  }

  const parts = [];

  parts.push(`
    <svg xmlns="http://www.w3.org/2000/svg"
      width="${width}" height="${height}"
      viewBox="0 0 ${width} ${height}">
  `);

  parts.push(`<rect width="${width}" height="${height}" fill="#f8fafc" />`);

  parts.push(`
    <text x="${cx}" y="48" text-anchor="middle"
      font-family="Inter, Arial" font-size="26" font-weight="800"
      fill="#0f172a">
      Continuity Field Dynamics
    </text>

    <text x="${cx}" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only bounded pressure flow and recoverability basin visibility
    </text>

    <text x="${cx}" y="118" text-anchor="middle"
      font-family="Inter, Arial" font-size="18" font-weight="800"
      fill="#0f172a">
      ${frame.label}
    </text>

    <text x="${cx}" y="146" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      ${frame.note}
    </text>
  `);

  parts.push(`
    <circle cx="${cx}" cy="${cy}" r="${basinRadius}"
      fill="#22c55e" opacity="0.045"
      stroke="#22c55e" stroke-width="${corridorWidth}"
      stroke-dasharray="14,10" />

    <circle cx="${cx}" cy="${cy}" r="${pressureRadius}"
      fill="#ef4444" opacity="0.16"
      stroke="#ef4444" stroke-width="4" />

    <circle cx="${cx - 250}" cy="${cy - 110}" r="58"
      fill="#0ea5e9" opacity="0.15" stroke="#0ea5e9" stroke-width="3" />

    <circle cx="${cx + 260}" cy="${cy - 90}" r="58"
      fill="#8b5cf6" opacity="0.15" stroke="#8b5cf6" stroke-width="3" />

    <circle cx="${cx - 210}" cy="${cy + 150}" r="58"
      fill="#eab308" opacity="0.15" stroke="#eab308" stroke-width="3" />

    <circle cx="${cx + 230}" cy="${cy + 150}" r="58"
      fill="#f97316" opacity="0.15" stroke="#f97316" stroke-width="3" />

    <line x1="${cx - 250}" y1="${cy - 110}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.28" />

    <line x1="${cx + 260}" y1="${cy - 90}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.28" />

    <line x1="${cx - 210}" y1="${cy + 150}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.28" />

    <line x1="${cx + 230}" y1="${cy + 150}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.28" />

    <text x="${cx}" y="${cy + 6}" text-anchor="middle"
      font-family="Inter, Arial" font-size="15" font-weight="800"
      fill="#0f172a">
      Pressure Center
    </text>

    <text x="${cx - 250}" y="${cy - 106}" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#0f172a">
      Oversight
    </text>

    <text x="${cx + 260}" y="${cy - 86}" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#0f172a">
      Dependency
    </text>

    <text x="${cx - 210}" y="${cy + 154}" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#0f172a">
      Fallback
    </text>

    <text x="${cx + 230}" y="${cy + 154}" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#0f172a">
      Recovery
    </text>
  `);

  parts.push(`
    <rect x="80" y="650" width="1040" height="78" rx="20"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="190" y="684" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      Center Pressure: ${pct(frame.centerPressure)}%
    </text>

    <text x="600" y="684" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      Basin Integrity: ${pct(frame.basinIntegrity)}%
    </text>

    <text x="1000" y="684" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      Corridor Elasticity: ${pct(frame.corridorElasticity)}%
    </text>

    <text x="${cx}" y="710" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      NON-CLAIM: Field dynamics do not predict, score, govern, authorize, or certify recoverability.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadContinuityFieldDynamics() {
  if (!svgFrame) {
    return;
  }

  const svg = renderContinuityFieldDynamicsSvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  svgFrame.src = URL.createObjectURL(blob);

  if (notesBox) {
    const frame = currentContinuityFieldFrame();

    notesBox.textContent =
      "Continuity Field Dynamics\n\n" +
      frame.label +
      "\n\n" +
      frame.note +
      "\n\nCenter pressure: " +
      Math.round(frame.centerPressure * 100) +
      "%\nBasin integrity: " +
      Math.round(frame.basinIntegrity * 100) +
      "%\nCorridor elasticity: " +
      Math.round(frame.corridorElasticity * 100) +
      "%\n\nThis view is bounded, deterministic, observer-only, and non-authoritative.";
  }

  resetZoom();
}

function nextContinuityFieldFrame() {
  continuityFieldIndex = Math.min(
    continuityFieldIndex + 1,
    continuityFieldFrames.length - 1
  );

  loadContinuityFieldDynamics();
}

function previousContinuityFieldFrame() {
  continuityFieldIndex = Math.max(
    continuityFieldIndex - 1,
    0
  );

  loadContinuityFieldDynamics();
}

function firstContinuityFieldFrame() {
  continuityFieldIndex = 0;
  loadContinuityFieldDynamics();
}

function lastContinuityFieldFrame() {
  continuityFieldIndex = continuityFieldFrames.length - 1;
  loadContinuityFieldDynamics();
}