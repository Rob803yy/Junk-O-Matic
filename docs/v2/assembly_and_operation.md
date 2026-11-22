# V2 assembly and operation draft

This is a review procedure, not a release to fabricate or deploy the drafts.

## Assembly review

Confirm orientation and datums, then compare the CAD layout with the physical
buggy. Inspect cart-to-frame and frame-to-chassis joints, current enclosure and
battery mounting, dock latch/retention, moving clearances and harness supports.
Measure actual interfaces and enter them with evidence before creating holes or
fabrication drawings. The model's wall/member dimensions are illustrative.
Verify component masses/positions before evaluating lean. No spring replacement,
preload change, new bracket or battery relocation was assumed in this draft.

## Electrical review

With sources disconnected, trace the proposed QET/WireViz nets against every
conductor. Confirm source polarity, source/branch protection, conductor ratings,
switch contacts and actual converter models/settings. Establish Uno power entry
and simultaneous USB/external supply behaviour before energizing the new setup.
No cross-domain ground or isolation is assumed. Compare measured rails/current
with the actual equipment requirements; no arbitrary fuse or cutoff value exists
in these files.

## Software preservation and bench sequence

1. Locate original sketches/build files; preserve existing readable firmware
   before uploading replacement code. Record file hashes and recovery outcome.
2. Resolve USB device recognition and capture current serial bytes/behaviour.
3. Review proposed protocol and pin map. Enable only verified sensor circuits.
4. Compile and bench-test acquisition, null/fault flags, sample timing and local
   feedback. Compile-only test pins are not an installed connection plan.
5. Configure the Pi's actual serial identity and run the logger manually. Check
   raw file, database, manifest and sensor sample counts. Replay proves software
   handling only.
6. Test unplug/replug, sensor timeout and graceful Ctrl+C/SIGTERM. Review outputs
   before enabling any startup service.
7. If a camera is installed, test capture separately and verify actual footage
   and alignment. Camera type and synchronization remain unresolved.

The firmware and Pi logger issue no drive-control commands. This source fact does
not prove that the current physical vehicle has no other control interfaces.

## Field use and shutdown

Carry forward historical loaded-motion evidence without extrapolating a payload
rating. Agree the load, offset, route and acceptable lean, then run controlled
checks in the verified physical configuration. Record changes and negative
results. Stop on loose mounts, shifting batteries, wiring interference or loss of
repeatable control/settling; these findings become verification records.

Stop logging cleanly and inspect final manifest status before shutting down the
Pi and disconnecting sources according to the actual reviewed power arrangement.
Archive original raw/video data outside Git with configuration IDs and hashes.
The old V1A five-session targets remain proposed requirements until reviewed for
this physical V2 and supported by real results.
