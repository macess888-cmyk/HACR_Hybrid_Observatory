from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
REVIEW = ROOT / "ai-boundary-review.html"


def test_ai_boundary_review_surface_exists():
    assert REVIEW.exists()


def test_ai_boundary_review_declares_required_inspection_sequence():
    text = REVIEW.read_text(encoding="utf-8")

    for surface in (
        "Components",
        "Relations",
        "Transitions",
        "Composition",
        "Authority",
        "Consequence",
        "Recovery",
    ):
        assert surface in text


def test_ai_boundary_review_preserves_hold_semantics():
    text = REVIEW.read_text(encoding="utf-8")
    assert "UNKNOWN" in text
    assert "HOLD" in text


def test_ai_boundary_review_declares_pilot_scope_and_price():
    text = REVIEW.read_text(encoding="utf-8")
    assert "CAD $250" in text
    assert "one workflow" in text.lower()


def test_homepage_links_to_ai_boundary_review():
    text = HOME.read_text(encoding="utf-8")
    assert 'href="ai-boundary-review.html"' in text
    assert "AI Boundary Review" in text
