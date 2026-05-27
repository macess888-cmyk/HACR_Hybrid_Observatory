const deltaReceipt =
  "../tools/frame_delta_overlay/output/frame_delta_overlay_receipt.json";

const deltaFrames = [
  {
    id: "frame_001_to_frame_002",
    label: "Delta 001 → 002 — Endpoint Pressure Increase",
    svg: "../tools/frame_delta_overlay/output/frame_001_baseline_visibility__to__frame_002_endpoint_pressure_increase.svg",
    json: "../tools/frame_delta_overlay/output/frame_001_baseline_visibility__to__frame_002_endpoint_pressure_increase.json"
  },
  {
    id: "frame_002_to_frame_003",
    label: "Delta 002 → 003 — Recovery Path Visibility Loss",
    svg: "../tools/frame_delta_overlay/output/frame_002_endpoint_pressure_increase__to__frame_003_recovery_path_visibility_loss.svg",
    json: "../tools/frame_delta_overlay/output/frame_002_endpoint_pressure_increase__to__frame_003_recovery_path_visibility_loss.json"
  },
  {
    id: "frame_003_to_frame_004",
    label: "Delta 003 → 004 — Backup Recoverability Reassertion",
    svg: "../tools/frame_delta_overlay/output/frame_003_recovery_path_visibility_loss__to__frame_004_backup_recoverability_reassertion.svg",
    json: "../tools/frame_delta_overlay/output/frame_003_recovery_path_visibility_loss__to__frame_004_backup_recoverability_reassertion.json"
  }
];

let deltaIndex = 0;

function currentDeltaFrame() {
  return deltaFrames[deltaIndex];
}

function deltaStatusText() {
  return `Delta ${deltaIndex + 1} / ${deltaFrames.length}`;
}

function loadDeltaFrame() {
  const delta = currentDeltaFrame();

  if (!delta || !svgFrame) {
    return;
  }

  pauseReplay();

  svgFrame.src = delta.svg;

  if (downloadJson) {
    downloadJson.href = delta.json;
    downloadJson.setAttribute("download", "");
  }

  if (downloadReceipt) {
    downloadReceipt.href = deltaReceipt;
    downloadReceipt.setAttribute("download", "");
  }

  if (notesBox) {
    notesBox.textContent =
      deltaStatusText() +
      "\n\n" +
      delta.label +
      "\n\nObserver-only deterministic frame-delta visibility.\n\nDelta overlays do not score, predict, govern, authorize, certify, or replace operators.";
  }

  resetZoom();
}

function nextDeltaFrame() {
  deltaIndex = Math.min(deltaIndex + 1, deltaFrames.length - 1);
  loadDeltaFrame();
}

function previousDeltaFrame() {
  deltaIndex = Math.max(deltaIndex - 1, 0);
  loadDeltaFrame();
}

function firstDeltaFrame() {
  deltaIndex = 0;
  loadDeltaFrame();
}

function lastDeltaFrame() {
  deltaIndex = deltaFrames.length - 1;
  loadDeltaFrame();
}