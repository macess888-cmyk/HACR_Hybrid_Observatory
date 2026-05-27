const scenarioSelect = document.getElementById("scenarioSelect");
const loadButton = document.getElementById("loadButton");
const openButton = document.getElementById("openButton");
const downloadJson = document.getElementById("downloadJson");
const downloadReceipt = document.getElementById("downloadReceipt");
const svgFrame = document.getElementById("svgFrame");

const fitToggle = document.getElementById("fitToggle");
const borderToggle = document.getElementById("borderToggle");
const claimToggle = document.getElementById("claimToggle");
const notesToggle = document.getElementById("notesToggle");

const zoomOutButton = document.getElementById("zoomOutButton");
const zoomResetButton = document.getElementById("zoomResetButton");
const zoomInButton = document.getElementById("zoomInButton");

const normalViewButton = document.getElementById("normalViewButton");
const focusViewButton = document.getElementById("focusViewButton");
const softViewButton = document.getElementById("softViewButton");

const viewerBox = document.getElementById("viewerBox");
const nonClaimBox = document.getElementById("nonClaimBox");
const sidePanel = document.getElementById("sidePanel");
const workspace = document.getElementById("workspace");
const notesBox = document.getElementById("notesBox");

let zoomLevel = 1;

const scenarios = [
  {
    id: "hospital_continuity",
    label: "Hospital Continuity",
    svg: "../scenarios/hospital_continuity/svg/hospital_continuity_topology.svg",
    json: "../scenarios/hospital_continuity/json/hospital_continuity_case_v1.json",
    receipt: "../scenarios/hospital_continuity/receipts/hospital_continuity_topology_receipt.json"
  },
  {
    id: "distributed_hospital_continuity",
    label: "Distributed Hospital Continuity",
    svg: "../scenarios/distributed_hospital_continuity/svg/distributed_hospital_continuity_topology.svg",
    json: "../scenarios/distributed_hospital_continuity/json/distributed_hospital_continuity_case_v1.json",
    receipt: "../scenarios/distributed_hospital_continuity/receipts/distributed_hospital_continuity_topology_receipt.json"
  },
  {
    id: "centralized_vs_distributed_healthcare",
    label: "Centralized vs Distributed Comparison",
    svg: "../comparison/svg/centralized_vs_distributed_healthcare.svg",
    json: "../comparison/receipts/centralized_vs_distributed_healthcare_receipt.json",
    receipt: "../comparison/receipts/centralized_vs_distributed_healthcare_receipt.json"
  },
  {
    id: "regional_supply_chain",
    label: "Regional Supply Chain",
    svg: "../assets/demo_maps/regional_supply_chain_topology.svg",
    json: "../tools/continuity_drift_visualizer/input/regional_supply_chain_case.json",
    receipt: "../tools/continuity_drift_visualizer/output/regional_supply_chain_topology_receipt.json"
  },
  {
    id: "cyber_recoverability",
    label: "Cyber Recoverability",
    svg: "../scenarios/cyber_recoverability/svg/cyber_recoverability_topology.svg",
    json: "../scenarios/cyber_recoverability/json/cyber_recoverability_case_v1.json",
    receipt: "../scenarios/cyber_recoverability/receipts/cyber_recoverability_topology_receipt.json"
  }
];

function populateScenarios() {
  scenarioSelect.innerHTML = "";

  scenarios.forEach((scenario) => {
    const option = document.createElement("option");
    option.value = scenario.id;
    option.textContent = scenario.label;
    scenarioSelect.appendChild(option);
  });

  scenarioSelect.value = "hospital_continuity";
  loadScenario();
}

function currentScenario() {
  return scenarios.find((scenario) => scenario.id === scenarioSelect.value);
}

function updateNotes(scenarioId) {
  if (!window.scenarioNotes) {
    notesBox.textContent = "Operational notes unavailable.";
    return;
  }

  notesBox.textContent = scenarioNotes[scenarioId] || "No operational notes available.";
}

function applyZoom() {
  const baseHeight = fitToggle.checked ? 820 : 620;

  viewerBox.style.height = `${baseHeight}px`;
  svgFrame.style.height = `${baseHeight / zoomLevel}px`;
  svgFrame.style.width = `${100 / zoomLevel}%`;
  svgFrame.style.transform = `scale(${zoomLevel})`;
  svgFrame.style.transformOrigin = "top left";
}

function zoomIn() {
  zoomLevel = Math.min(zoomLevel + 0.1, 1.8);
  applyZoom();
}

function zoomOut() {
  zoomLevel = Math.max(zoomLevel - 0.1, 0.7);
  applyZoom();
}

function resetZoom() {
  zoomLevel = 1;
  applyZoom();
}

function loadScenario() {
  const scenario = currentScenario();

  if (!scenario) {
    return;
  }

  svgFrame.src = scenario.svg;

  downloadJson.href = scenario.json;
  downloadJson.setAttribute("download", "");

  downloadReceipt.href = scenario.receipt;
  downloadReceipt.setAttribute("download", "");

  updateNotes(scenario.id);
  resetZoom();
}

function openSvg() {
  const scenario = currentScenario();

  if (!scenario) {
    return;
  }

  window.open(scenario.svg, "_blank");
}

function setViewMode(mode) {
  viewerBox.classList.remove("viewNormal", "viewFocus", "viewSoft");
  viewerBox.classList.add(mode);
}

function applyViewerControls() {
  viewerBox.classList.toggle("noBorder", !borderToggle.checked);
  nonClaimBox.classList.toggle("isHidden", !claimToggle.checked);

  if (notesToggle.checked) {
    sidePanel.classList.remove("isHidden");
    workspace.classList.remove("notesHidden");
  } else {
    sidePanel.classList.add("isHidden");
    workspace.classList.add("notesHidden");
  }

  applyZoom();
}

loadButton.addEventListener("click", loadScenario);
openButton.addEventListener("click", openSvg);
scenarioSelect.addEventListener("change", loadScenario);

fitToggle.addEventListener("change", applyViewerControls);
borderToggle.addEventListener("change", applyViewerControls);
claimToggle.addEventListener("change", applyViewerControls);
notesToggle.addEventListener("change", applyViewerControls);

zoomOutButton.addEventListener("click", zoomOut);
zoomResetButton.addEventListener("click", resetZoom);
zoomInButton.addEventListener("click", zoomIn);

normalViewButton.addEventListener("click", () => setViewMode("viewNormal"));
focusViewButton.addEventListener("click", () => setViewMode("viewFocus"));
softViewButton.addEventListener("click", () => setViewMode("viewSoft"));

setViewMode("viewNormal");
populateScenarios();
applyViewerControls();