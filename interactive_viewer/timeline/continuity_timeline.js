const continuityTimelineEvents = [
  {
    id: "event_001",
    label: "t1 — Baseline Visibility",
    frame: 0,
    type: "baseline",
    pressure: "distributed",
    corridor: "visible",
    description:
      "Continuity visibility remains distributed across the field. Recoverability basin remains broadly visible."
  },
  {
    id: "event_002",
    label: "t2 — Endpoint / Dependency Pressure Increase",
    frame: 1,
    type: "pressure_escalation",
    pressure: "increasing",
    corridor: "narrowing",
    description:
      "Dependency pressure increases while fallback and oversight visibility begin narrowing."
  },
  {
    id: "event_003",
    label: "t3 — Recoverability Contraction",
    frame: 2,
    type: "contraction",
    pressure: "concentrated",
    corridor: "fragile",
    description:
      "Recoverability corridor visibility contracts and localization visibility degrades under concentrated pressure."
  },
  {
    id: "event_004",
    label: "t4 — Partial Visibility Reassertion",
    frame: 3,
    type: "partial_reassertion",
    pressure: "partially reduced",
    corridor: "visible but constrained",
    description:
      "Fallback visibility partially reasserts without asserting recovery success or operational restoration."
  }
];

let timelineIndex = 0;

function currentTimelineEvent() {
  return continuityTimelineEvents[timelineIndex];
}

function timelineColor(type) {
  const colors = {
    baseline: "#22c55e",
    pressure_escalation: "#eab308",
    contraction: "#ef4444",
    partial_reassertion: "#0ea5e9"
  };

  return colors[type] || "#64748b";
}

function renderContinuityTimelineSvg() {
  const width = 1200;
  const height = 820;
  const cx = width / 2;
  const event = currentTimelineEvent();

  const startX = 210;
  const endX = 990;
  const timelineY = 380;
  const spacing = (endX - startX) / (continuityTimelineEvents.length - 1);

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
      Continuity Timeline / Event Trace
    </text>

    <text x="${cx}" y="78" text-anchor="middle"
      font-family="Inter, Arial" font-size="14"
      fill="#475569">
      Observer-only replay-linked event chronology and interruption viability trace visibility
    </text>
  `);

  parts.push(`
    <rect x="120" y="125" width="960" height="150" rx="22"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${cx}" y="164" text-anchor="middle"
      font-family="Inter, Arial" font-size="19" font-weight="800"
      fill="#0f172a">
      ${event.label}
    </text>

    <text x="${cx}" y="198" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      Pressure: ${event.pressure} | Corridor: ${event.corridor}
    </text>

    <text x="${cx}" y="232" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      ${event.description}
    </text>
  `);

  parts.push(`
    <line x1="${startX}" y1="${timelineY}" x2="${endX}" y2="${timelineY}"
      stroke="#64748b" stroke-width="5" opacity="0.25"
      stroke-linecap="round" />
  `);

  continuityTimelineEvents.forEach((item, index) => {
    const x = startX + spacing * index;
    const color = timelineColor(item.type);
    const isActive = index === timelineIndex;
    const r = isActive ? 30 : 22;
    const opacity = isActive ? 0.35 : 0.18;

    parts.push(`
      <circle cx="${x}" cy="${timelineY}" r="${r}"
        fill="${color}" opacity="${opacity}"
        stroke="${color}" stroke-width="4" />

      <text x="${x}" y="${timelineY + 60}" text-anchor="middle"
        font-family="Inter, Arial" font-size="12" font-weight="800"
        fill="#0f172a">
        t${index + 1}
      </text>

      <text x="${x}" y="${timelineY + 82}" text-anchor="middle"
        font-family="Inter, Arial" font-size="11"
        fill="#475569">
        ${item.type.replaceAll("_", " ")}
      </text>
    `);
  });

  parts.push(`
    <rect x="180" y="535" width="840" height="105" rx="22"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${cx}" y="572" text-anchor="middle"
      font-family="Inter, Arial" font-size="17" font-weight="800"
      fill="#0f172a">
      Observability Lineage Marker
    </text>

    <text x="${cx}" y="604" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      Replay frame index: ${event.frame + 1} / ${continuityTimelineEvents.length}
    </text>

    <text x="${cx}" y="628" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      Event trace is a bounded inspection surface, not a causal proof or operational instruction.
    </text>
  `);

  parts.push(`
    <rect x="245" y="700" width="710" height="54" rx="18"
      fill="#ffffff" stroke="#cbd5e1" />

    <text x="${cx}" y="724" text-anchor="middle"
      font-family="Inter, Arial" font-size="13" font-weight="800"
      fill="#475569">
      NON-CLAIM: Timeline trace does not predict, score, govern, authorize, certify, or prove causality.
    </text>

    <text x="${cx}" y="744" text-anchor="middle"
      font-family="Inter, Arial" font-size="13"
      fill="#475569">
      It provides bounded observer-only event chronology visibility.
    </text>
  `);

  parts.push("</svg>");

  return parts.join("\n");
}

function loadContinuityTimeline() {
  if (!svgFrame) {
    return;
  }

  const svg = renderContinuityTimelineSvg();
  const blob = new Blob([svg], {
    type: "image/svg+xml"
  });

  svgFrame.src = URL.createObjectURL(blob);

  if (notesBox) {
    const event = currentTimelineEvent();

    notesBox.textContent =
      "Continuity Timeline / Event Trace\n\n" +
      event.label +
      "\n\n" +
      event.description +
      "\n\nPressure: " +
      event.pressure +
      "\nCorridor: " +
      event.corridor +
      "\nReplay frame index: " +
      (event.frame + 1) +
      " / " +
      continuityTimelineEvents.length +
      "\n\nTimeline trace remains observer-only and non-authoritative.";
  }

  resetZoom();
}

function nextTimelineEvent() {
  timelineIndex = Math.min(
    timelineIndex + 1,
    continuityTimelineEvents.length - 1
  );

  loadContinuityTimeline();
}

function previousTimelineEvent() {
  timelineIndex = Math.max(
    timelineIndex - 1,
    0
  );

  loadContinuityTimeline();
}

function firstTimelineEvent() {
  timelineIndex = 0;
  loadContinuityTimeline();
}

function lastTimelineEvent() {
  timelineIndex = continuityTimelineEvents.length - 1;
  loadContinuityTimeline();
}