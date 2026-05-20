# Update Loop Checklist

## Check 1

Does render directly call setState?

If yes:

FIX.

## Check 2

Does useEffect update a dependency it watches?

If yes:

FIX.

## Check 3

Does useEffect have no dependency array while updating state?

If yes:

FIX.

## Check 4

Does dependency array contain unstable objects, arrays, or functions?

If yes:

HOLD or FIX.

## Check 5

Does parent update child, then child update parent?

If yes:

FIX.

## Check 6

Is the cause unknown?

If yes:

HOLD.

## Core Reduction

UNKNOWN -> HOLD.