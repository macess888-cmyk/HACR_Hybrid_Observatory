# Recoverability Demo Case

## Scenario

A small business ecosystem appears operationally stable.

However:

- supplier concentration increases
- delivery fragmentation increases
- manual coordination load increases
- recovery windows narrow
- interruption survivability decreases

without immediate visible failure.

---

## Sample Input

```json
{
  "dependency_concentration": 0.84,
  "manual_compensation": true,
  "supplier_fragility": 0.79,
  "interruption_recovery_window_days": 2,
  "visible_operational_status": "stable"
}