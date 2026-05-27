const replayReceipt =
  "../tools/continuity_replay_engine/output/cyber_recoverability_replay_receipt.json";

const replayFrames = [
  {
    id: "frame_001_baseline_visibility",
    label: "Frame 001 — Baseline Visibility",
    svg: "../tools/continuity_replay_engine/output/frame_001_baseline_visibility.svg",
    json: "../tools/continuity_replay_engine/frames/frame_001_baseline_visibility.json"
  },
  {
    id: "frame_002_endpoint_pressure_increase",
    label: "Frame 002 — Endpoint Pressure Increase",
    svg: "../tools/continuity_replay_engine/output/frame_002_endpoint_pressure_increase.svg",
    json: "../tools/continuity_replay_engine/frames/frame_002_endpoint_pressure_increase.json"
  },
  {
    id: "frame_003_recovery_path_visibility_loss",
    label: "Frame 003 — Recovery Path Visibility Loss",
    svg: "../tools/continuity_replay_engine/output/frame_003_recovery_path_visibility_loss.svg",
    json: "../tools/continuity_replay_engine/frames/frame_003_recovery_path_visibility_loss.json"
  },
  {
    id: "frame_004_backup_recoverability_reassertion",
    label: "Frame 004 — Backup Recoverability Reassertion",
    svg: "../tools/continuity_replay_engine/output/frame_004_backup_recoverability_reassertion.svg",
    json: "../tools/continuity_replay_engine/frames/frame_004_backup_recoverability_reassertion.json"
  }
];

let replayIndex = 0;
let replayTimer = null;

function currentReplayFrame() {
  return replayFrames[replayIndex];
}

function replayStatusText() {
  return `Replay ${replayIndex + 1} / ${replayFrames.length}`;
}

function loadReplayFrame() {
  const frame = currentReplayFrame();

  if (!frame || !svgFrame) {
    return;
  }

  svgFrame.src = frame.svg;

  if (downloadJson) {
    downloadJson.href = frame.json;
    downloadJson.setAttribute("download", "");
  }

  if (downloadReceipt) {
    downloadReceipt.href = replayReceipt;
    downloadReceipt.setAttribute("download", "");
  }

  if (notesBox) {
    notesBox.textContent =
      replayStatusText() +
      "\n\n" +
      frame.label +
      "\n\nObserver-only deterministic replay navigation.\n\nThis replay does not predict, govern, authorize, certify, simulate authority, or replace operators.";
  }

  resetZoom();
}

function nextReplayFrame() {
  replayIndex = Math.min(replayIndex + 1, replayFrames.length - 1);
  loadReplayFrame();
}

function previousReplayFrame() {
  replayIndex = Math.max(replayIndex - 1, 0);
  loadReplayFrame();
}

function firstReplayFrame() {
  replayIndex = 0;
  loadReplayFrame();
}

function lastReplayFrame() {
  replayIndex = replayFrames.length - 1;
  loadReplayFrame();
}

function playReplay() {
  pauseReplay();

  loadReplayFrame();

  replayTimer = window.setInterval(() => {
    if (replayIndex >= replayFrames.length - 1) {
      pauseReplay();
      return;
    }

    replayIndex += 1;
    loadReplayFrame();
  }, 1800);
}

function pauseReplay() {
  if (replayTimer) {
    window.clearInterval(replayTimer);
    replayTimer = null;
  }
}