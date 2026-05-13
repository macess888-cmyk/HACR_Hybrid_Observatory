# Reviewer Quickstart

This repository is an observer-restricted continuity survivability observatory.

It does not:
- govern execution
- authorize action
- certify systems
- enforce runtime behavior
- provide production safety guarantees

It produces bounded, reproducible inspection artifacts under controlled conditions.

---

## Purpose

The reviewer quickstart provides the shortest path to regenerate the current runtime survivability outputs locally.

The goal is not to trust the repository as authority.

The goal is to test whether the same controlled inputs reproduce the same PASS / HOLD / FAIL observations.

---

## Run

From the repository root:

```bash
python runtime/runtime_survivability_harness.py
python runtime/distributed_invalidation_simulator.py