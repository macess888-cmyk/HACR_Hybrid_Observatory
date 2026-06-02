# Standing Failure Atlas

Observer-only failure surface registry.

## SF_0001 — Candidate Promoted Before Pressure

A candidate is treated as standing-bearing before it survives pressure.

Failure:

Candidate → Standing

without pressure.

## SF_0002 — Standing Assumed From Observation

Observation is mistaken for standing.

Failure:

Observation → Standing

## SF_0003 — Standing Assumed From Persistence

A candidate persists over time and is treated as established.

Failure:

Persistence → Standing

## SF_0004 — Failure Interpreted As Replacement

All candidates fail, then a new candidate is automatically promoted.

Failure:

A fails  
B fails  
C fails  
↓  
D promoted

## SF_0005 — Unknown Treated As Error

Unknown is treated as a system defect rather than an admissible state.

Failure:

UNKNOWN → ERROR

instead of:

UNKNOWN → HOLD

## SF_0006 — Pressure Mistaken For Authority

Pressure produces response, and response is treated as authorization.

Failure:

Pressure Response → Authority

## SF_0007 — Standing Hidden Inside Authority

Authority is invoked before standing is localized.

Failure:

Authority first  
Standing later

## SF_0008 — Refusal Removed From Outcome Space

System permits only proceed or hold.

Failure:

PROCEED / HOLD

without:

REFUSE

## SF_0009 — Hold Removed From Outcome Space

System permits only proceed or refuse.

Failure:

PROCEED / REFUSE

without:

HOLD

## SF_0010 — Proceed Privileged By Default

Proceed becomes the preferred outcome even when standing is unresolved.

Failure:

Unresolved → Proceed