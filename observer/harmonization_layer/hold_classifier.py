from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


State = Literal["ADMISSIBLE", "HOLD", "INCOMPATIBLE"]


@dataclass(frozen=True)
class Signal:
    source: str
    domain: str
    provenance_clear: bool
    authority_clear: bool
    containment_clear: bool
    recovery_path_clear: bool
    compatible: bool


def classify_signal(signal: Signal) -> State:
    if not signal.compatible:
        return "INCOMPATIBLE"

    if not (
        signal.provenance_clear
        and signal.authority_clear
        and signal.containment_clear
        and signal.recovery_path_clear
    ):
        return "HOLD"

    return "ADMISSIBLE"