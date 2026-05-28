const atlasDomains = [
  {
    id: "healthcare",
    label: "Healthcare Continuity",
    description:
      "Hospital, distributed care, intake, staffing, records, and backup continuity visibility.",
    scenarios: [
      "hospital_continuity",
      "distributed_hospital_continuity"
    ]
  },
  {
    id: "cyber",
    label: "Cyber Recoverability",
    description:
      "Identity, endpoint, cloud, SOC, backup, and restore-path continuity visibility.",
    scenarios: [
      "cyber_recoverability"
    ]
  },
  {
    id: "ai_oversight",
    label: "AI Oversight Continuity",
    description:
      "Human oversight, policy gate, fallback path, audit record, and dependency opacity visibility.",
    scenarios: [
      "ai_oversight_continuity"
    ]
  },
  {
    id: "energy",
    label: "Energy Grid Recoverability",
    description:
      "Substation, transformer concentration, backup generation, control-room, and distribution continuity visibility.",
    scenarios: [
      "energy_grid_recoverability"
    ]
  },
  {
    id: "emergency",
    label: "Emergency Response Continuity",
    description:
      "Dispatch, mobile response, hospital intake, radio communications, road access, and mutual aid visibility.",
    scenarios: [
      "emergency_response_continuity"
    ]
  },
  {
    id: "supply_chain",
    label: "Regional Supply Chain",
    description:
      "Supplier, route, local business, customer demand, coordination, and backup supply visibility.",
    scenarios: [
      "regional_supply_chain"
    ]
  },
  {
    id: "comparison",
    label: "Comparison Views",
    description:
      "Side-by-side continuity comparison surfaces for centralized and distributed topologies.",
    scenarios: [
      "centralized_vs_distributed_healthcare"
    ]
  }
];

function atlasSummaryText() {
  return atlasDomains
    .map((domain) => {
      return (
        domain.label +
        "\n" +
        domain.description +
        "\nScenarios: " +
        domain.scenarios.join(", ")
      );
    })
    .join("\n\n");
}

function showAtlasOverview() {
  if (!notesBox) {
    return;
  }

  notesBox.textContent =
    "Observatory Atlas Navigation\n\n" +
    atlasSummaryText() +
    "\n\nAtlas mode is observer-only. It groups continuity inspection surfaces without authorizing, scoring, predicting, or certifying any scenario.";
}

function loadAtlasDomain(domainId) {
  const domain = atlasDomains.find((item) => item.id === domainId);

  if (!domain || !domain.scenarios.length) {
    return;
  }

  const firstScenario = domain.scenarios[0];

  if (scenarioSelect) {
    scenarioSelect.value = firstScenario;
    loadScenario();
  }

  if (notesBox) {
    notesBox.textContent =
      domain.label +
      "\n\n" +
      domain.description +
      "\n\nLoaded scenario:\n" +
      firstScenario +
      "\n\nAtlas traversal remains observer-only and non-authoritative.";
  }
}