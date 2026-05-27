# GitHub Pages Deployment

## Purpose

This deployment publishes the HACR Hybrid Observatory public viewer as:

bounded deterministic continuity cartography.

---

# Current Public Components

- interactive viewer
- replay traversal
- frame delta overlays
- deterministic SVG observability
- replay receipts
- delta receipts

---

# GitHub Pages Structure

Current deployment root:

docs_site/

Viewer entry:

docs_site/index.html

Interactive viewer:

interactive_viewer/index.html

---

# Deployment Preparation

Before deployment verify:

- all SVGs render correctly
- replay traversal functions
- delta overlays function
- viewer controls function
- replay receipts exist
- delta receipts exist
- no broken relative paths

---

# Suggested Deployment Flow

## Option 1 — docs/ deployment

Move public deployment files into:

docs/

Enable:

GitHub
→ Settings
→ Pages
→ Deploy from branch
→ /docs

---

## Option 2 — gh-pages branch

Create:

gh-pages branch

Publish static deployment artifacts there.

---

# Current Boundary

The public observatory remains:

- observer-only
- deterministic
- bounded
- non-authoritative
- externally reviewable

---

# NON-CLAIMS

The public deployment does not:

- predict operational futures
- govern systems
- authorize execution
- certify recoverability
- replace operators
- provide operational guarantees

The deployment provides:

bounded operational continuity visibility only.