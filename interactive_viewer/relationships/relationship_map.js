const relationshipGroups = [
  {
    id: "human_oversight_visibility",
    label: "Human Oversight Visibility",
    description:
      "Surfaces where human interpretation, coordination, or intervention visibility narrows while operations may still appear continuous.",
    scenarios: [
      "hospital_continuity",
      "distributed_hospital_continuity",
      "ai_oversight_continuity",
      "emergency_response_continuity"
    ]
  },
  {
    id: "dependency_concentration",
    label: "Dependency Concentration",
    description:
      "Surfaces where continuity depends on a concentrated node, hub, provider, or coordination point.",
    scenarios: [
      "cyber_recoverability",
      "energy_grid_recoverability",
      "regional_supply_chain",
      "centralized_vs_distributed_healthcare"
    ]
  },
  {
    id: "fallback_corridor_visibility",
    label: "Fallback Corridor Visibility",
    description:
      "Surfaces where recoverability depends on whether fallback routes remain visible, localizable, and materially reachable.",
    scenarios: [
      "cyber_recoverability",
      "energy_grid_recoverability",
      "emergency_response_continuity",
      "distributed_hospital_continuity"
    ]
  },
  {
    id: "shadow_dependency_pressure",
    label: "Shadow Dependency Pressure",
    description:
      "Surfaces where hidden or external dependencies may preserve operational appearance while narrowing recoverability.",
    scenarios: [
      "regional_supply_chain",
      "cyber_recoverability",
      "ai_oversight_continuity",
      "energy_grid_recoverability"
    ]
  }
];

function relationshipSummaryText() {
  return relationshipGroups
    .map((group) => {
      return (
        group.label +
        "\n" +
        group.description +
        "\nRelated scenarios: " +
        group.scenarios.join(", ")
      );
    })
    .join("\n\n");
}

function showRelationshipOverview() {
  if (!notesBox) {
    return;
  }

  notesBox.textContent =
    "Topology Relationship Mapping\n\n" +
    relationshipSummaryText() +
    "\n\nRelationship mapping is observer-only. It exposes shared continuity pressure surfaces without scoring, predicting, authorizing, certifying, or governing any scenario.";
}

function loadRelationshipGroup(groupId) {
  const group = relationshipGroups.find((item) => item.id === groupId);

  if (!group || !group.scenarios.length) {
    return;
  }

  const firstScenario = group.scenarios[0];

  if (scenarioSelect) {
    scenarioSelect.value = firstScenario;

    if (typeof loadScenario === "function") {
      loadScenario();
    }
  }

  const scenarioLines = group.scenarios
    .map((scenario) => "• " + scenario)
    .join("\n");

  if (notesBox) {
    notesBox.textContent =
      group.label +
      "\n\n" +
      group.description +
      "\n\nLoaded scenario:\n" +
      firstScenario +
      "\n\nRelated scenarios:\n" +
      scenarioLines +
      "\n\nRelationship traversal remains observer-only and non-authoritative.";
  }
}

function relationshipGroupsForScenario(scenarioId) {
  return relationshipGroups.filter((group) =>
    group.scenarios.includes(scenarioId)
  );
}

function relationshipContextText(scenarioId) {
  const groups = relationshipGroupsForScenario(scenarioId);

  if (!groups.length) {
    return "No mapped relationship groups.";
  }

  return groups
    .map((group) => {
      return (
        group.label +
        ": " +
        group.description
      );
    })
    .join("\n\n");
}

function appendRelationshipContext(scenarioId) {
  if (!notesBox) {
    return;
  }

  const existing = notesBox.textContent || "";

  notesBox.textContent =
    existing +
    "\n\n--- Relationship Context ---\n\n" +
    relationshipContextText(scenarioId);
}