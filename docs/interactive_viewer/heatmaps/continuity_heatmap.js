const continuityHeatmapFrames = [
  {
    label: "Heatmap t1 — Distributed Pressure",
    center: 0.34,
    oversight: 0.42,
    dependency: 0.48,
    fallback: 0.31,
    recovery: 0.36,
    note: "Pressure is distributed across the field with no single dominant concentration."
  },
  {
    label: "Heatmap t2 — Dependency Warming",
    center: 0.56,
    oversight: 0.51,
    dependency: 0.73,
    fallback: 0.44,
    recovery: 0.49,
    note: "Dependency surface begins carrying higher intensity while fallback pressure rises."
  },
  {
    label: "Heatmap t3 — Basin Stress Concentration",
    center: 0.84,
    oversight: 0.69,
    dependency: 0.91,
    fallback: 0.72,
    recovery: 0.67,
    note: "Pressure concentrates around dependency and center surfaces; basin stress density increases."
  },
  {
    label: "Heatmap t4 — Partial Cooling",
    center: 0.58,
    oversight: 0.54,
    dependency: 0.64,
    fallback: 0.46,
    recovery: 0.52,
    note: "Intensity partially cools, but pressure remains visible across recovery and dependency surfaces."
  }
];

let heatmapIndex = 0;

function currentHeatmapFrame() {
  return continuityHeatmapFrames[heatmapIndex];
}

function heatColor(value) {
  if (value >= 0.8) {
    return "#ef4444";
  }

  if (value >= 0.6) {
    return "#f97316";
  }

  if (value >= 0.4) {
    return "#eab308";
  }

  return "#22c55e";
}

function heatRadius(value) {
  return 45 + value * 105;
}

function renderContinuityHeatmapSvg() {
  const width = 1200;
  const height = 820;
  const cx = width / 2;
  const cy = height / 2 + 20;
  const frame = currentHeatmapFrame();

  const surfaces = [
    {
      label: "Center Pressure",
      x: cx,
      y: cy,
      value: frame.center
    },
    {
      label: "Oversight",
      x: cx - 260,
      y: cy - 120,
      value: frame.oversight
    },
    {
      label: "Dependency",
      x: cx + 260,
      y: cy - 100,
      value: frame.dependency
    },
    {
      label: "Fallback",
      x: cx - 230,
      y: cy + 155,
      value: frame.fallback
    },
    {
      label: "Recovery",
      x: cx + 240,
      y: cy + 155,
      value: frame.recovery
    }
  ];

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
      Continuity Heatmap Surface
    </text>

    <text x="${cx}" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only pressure intensity and recoverability stress distribution visibility
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

  surfaces.forEach((surface) => {
    const color = heatColor(surface.value);
    const radius = heatRadius(surface.value);
    const percent = Math.round(surface.value * 100);

    parts.push(`
      <circle cx="${surface.x}" cy="${surface.y}" r="${radius}"
        fill="${color}" opacity="0.10" />

      <circle cx="${surface.x}" cy="${surface.y}" r="${Math.max(32, radius * 0.42)}"
        fill="${color}" opacity="0.22" stroke="${color}" stroke-width="3" />

      <text x="${surface.x}" y="${surface.y - 4}" text-anchor="middle"
        font-family="Inter, Arial" font-size="14" font-weight="800"
        fill="#0f172a">
        ${surface.label}
      </text>

      <text x="${surface.x}" y="${surface.y + 18}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12"
        fill="#475569">
        ${percent}% intensity
      </text>
    `);
  });

  parts.push(`
    <line x1="${cx - 260}" y1="${cy - 120}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.18" />

    <line x1="${cx + 260}" y1="${cy - 100}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.18" />

    <line x1="${cx - 230}" y1="${cy + 155}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.18" />

    <line x1="${cx + 240}" y1="${cy + 155}" x2="${cx}" y2="${cy}"
      stroke="#64748b" stroke-width="4" opacity="0.18" />
  `);

  parts.push(`
    <rect x="210" y="680" width="780" height="64" rx="18"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${cx}" y="706" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      NON-CLAIM: Heatmaps do not score, predict, govern, authorize, or certify recoverability.
    </text>

    <text x="${cx}" y="728" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      They provide bounded observer-only intensity distribution visibility.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadContinuityHeatmap() {
  if (!svgFrame) {
    return;
  }

  const svg = renderContinuityHeatmapSvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  svgFrame.src = URL.createObjectURL(blob);

  if (notesBox) {
    const frame = currentHeatmapFrame();

    notesBox.textContent =
      "Continuity Heatmap Surface\n\n" +
      frame.label +
      "\n\n" +
      frame.note +
      "\n\nCenter pressure: " +
      Math.round(frame.center * 100) +
      "%\nOversight intensity: " +
      Math.round(frame.oversight * 100) +
      "%\nDependency intensity: " +
      Math.round(frame.dependency * 100) +
      "%\nFallback intensity: " +
      Math.round(frame.fallback * 100) +
      "%\nRecovery intensity: " +
      Math.round(frame.recovery * 100) +
      "%\n\nThis heatmap is observer-only, bounded, deterministic, and non-authoritative.";
  }

  resetZoom();
}

function nextHeatmapFrame() {
  heatmapIndex = Math.min(
    heatmapIndex + 1,
    continuityHeatmapFrames.length - 1
  );

  loadContinuityHeatmap();
}

function previousHeatmapFrame() {
  heatmapIndex = Math.max(
    heatmapIndex - 1,
    0
  );

  loadContinuityHeatmap();
}

function firstHeatmapFrame() {
  heatmapIndex = 0;
  loadContinuityHeatmap();
}

function lastHeatmapFrame() {
  heatmapIndex = continuityHeatmapFrames.length - 1;
  loadContinuityHeatmap();
}