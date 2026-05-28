let synchronizedIndex = 0;

const synchronizedFrameCount = 4;

function synchronizedStatusText() {
  return `Synchronized frame ${synchronizedIndex + 1} / ${synchronizedFrameCount}`;
}

function applySynchronizedIndex() {
  replayIndex = synchronizedIndex;
  deltaIndex = Math.min(synchronizedIndex, deltaFrames.length - 1);
  temporalDriftIndex = synchronizedIndex;
  continuityFieldIndex = synchronizedIndex;
}

function loadSynchronizedReplay() {
  applySynchronizedIndex();
  loadReplayFrame();

  if (notesBox) {
    notesBox.textContent =
      synchronizedStatusText() +
      "\n\nSynchronized Replay View\n\n" +
      "Replay, delta, temporal drift, and field dynamics are aligned to the same bounded frame index.\n\n" +
      "This synchronization does not predict, govern, authorize, score, certify, or replace operators.";
  }
}

function loadSynchronizedDelta() {
  applySynchronizedIndex();
  loadDeltaFrame();

  if (notesBox) {
    notesBox.textContent =
      synchronizedStatusText() +
      "\n\nSynchronized Delta View\n\n" +
      "Delta visibility is aligned with replay, temporal drift, and field dynamics indices.\n\n" +
      "This synchronization remains observer-only and non-authoritative.";
  }
}

function loadSynchronizedTemporalDrift() {
  applySynchronizedIndex();
  loadTemporalCorridorDrift();

  if (notesBox) {
    notesBox.textContent =
      synchronizedStatusText() +
      "\n\nSynchronized Temporal Drift View\n\n" +
      "Temporal corridor drift is aligned with replay and field dynamics frame position.\n\n" +
      "This view provides bounded continuity movement visibility only.";
  }
}

function loadSynchronizedFieldDynamics() {
  applySynchronizedIndex();
  loadContinuityFieldDynamics();

  if (notesBox) {
    notesBox.textContent =
      synchronizedStatusText() +
      "\n\nSynchronized Field Dynamics View\n\n" +
      "Continuity field dynamics are aligned with replay and temporal drift position.\n\n" +
      "This view provides bounded pressure-flow visibility only.";
  }
}

function nextSynchronizedFrame() {
  synchronizedIndex = Math.min(
    synchronizedIndex + 1,
    synchronizedFrameCount - 1
  );

  loadSynchronizedReplay();
}

function previousSynchronizedFrame() {
  synchronizedIndex = Math.max(
    synchronizedIndex - 1,
    0
  );

  loadSynchronizedReplay();
}

function firstSynchronizedFrame() {
  synchronizedIndex = 0;
  loadSynchronizedReplay();
}

function lastSynchronizedFrame() {
  synchronizedIndex = synchronizedFrameCount - 1;
  loadSynchronizedReplay();
}

function loadSynchronizedFrame() {
  loadSynchronizedReplay();
}