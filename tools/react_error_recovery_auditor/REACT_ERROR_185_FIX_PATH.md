# React Error 185 Fix Path

## Meaning

React error #185 commonly indicates maximum update depth exceeded.

This usually means a component repeatedly triggers state updates during render/effect execution.

## Common Causes

- setState called during render
- useEffect updates state watched by its own dependency array
- missing dependency array
- unstable object dependency
- unstable array dependency
- unstable function dependency
- recursive parent/child state update loop

## Fix Path

1. Find the component that last changed.
2. Search for setState calls.
3. Check whether setState happens during render.
4. Check useEffect dependency arrays.
5. Check whether the effect updates a watched dependency.
6. Stabilize objects/functions with useMemo/useCallback only when needed.
7. Add guards before state updates.
8. Re-run.

## Core Reduction

State updates must not recursively recreate their own trigger.