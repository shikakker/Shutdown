# Product Completion Status — Shutdown Planner

Canonical repository: `shikakker/Shutdown`  
Completion branch: `portfolio-improvements-2026-08`  
Draft PR: #2 — do not merge or promote production automatically.

## T01–T10 — Core tasks

| ID | Status | Task |
| --- | --- | --- |
| T01 | DONE | Replace immediate destructive shutdown examples with a non-executing planner. |
| T02 | DONE | Planner never invokes shell/subprocess/system shutdown commands. |
| T03 | DONE | Require a delay of at least 60 seconds and at most 24 hours. |
| T04 | DONE | Validate local/IP/DNS target before generating a plan. |
| T05 | DONE | Validate remote Linux SSH username before rendering a command. |
| T06 | DONE | Never add force-close flags to Windows plans. |
| T07 | DONE | Always print a platform-appropriate abort command. |
| T08 | DONE | Remove guidance to enable Remote Registry/firewall rules automatically. |
| T09 | DONE | Add standard-library unit tests and Python compile CI. |
| T10 | DEFERRED WITH REASON | Actual execution remains operator-owned and intentionally outside this repository. |

## I01–I10 — Improvements

| ID | Status | Improvement |
| --- | --- | --- |
| I01 | DONE | Explicit “DRY RUN ONLY” output. |
| I02 | DONE | Windows shutdown/restart plans supported. |
| I03 | DONE | Linux shutdown/restart plans supported. |
| I04 | DONE | Remote Windows target rendering. |
| I05 | DONE | Remote Linux SSH plan rendering. |
| I06 | DONE | Safe fixed maintenance warning. |
| I07 | DONE | IP address validation via standard library. |
| I08 | DONE | Hostname/username character bounds reduce command-injection risk in copied plans. |
| I09 | DONE | English README rewritten around authorization/preflight/recovery. |
| I10 | DONE | Russian guide rewritten to the same non-destructive boundary. |

## F01–F10 — Product features

| ID | Status | Feature |
| --- | --- | --- |
| F01 | DONE | Generate local Windows shutdown plan. |
| F02 | DONE | Generate local Windows restart plan. |
| F03 | DONE | Generate remote Windows maintenance plan. |
| F04 | DONE | Generate local Linux shutdown plan. |
| F05 | DONE | Generate local Linux restart plan. |
| F06 | DONE | Generate remote Linux SSH plan. |
| F07 | DONE | Print abort command. |
| F08 | DONE | Reject unsafe target/user input. |
| F09 | DONE | Reject immediate/overlong delays. |
| F10 | INTENTIONALLY NOT IMPLEMENTED | Automatic execution/remote-control service is excluded to keep authorization and destructive action under the operator's existing admin environment. |

## Latest P0/P1 — unsafe immediate/destructive guidance

The previous repository primarily consisted of copy-paste commands such as `shutdown /s /t 0`, `shutdown now`, forced application close and remote-administration enablement. There was no target validation, delay floor, abort flow or execution boundary.

The repository now contains a testable planner that only prints a reviewed maintenance plan. It cannot execute the command, requires a non-immediate delay, validates remote target/user syntax and always emits an abort command.

No device was shut down or restarted; no remote service/firewall was enabled; no credential, merge or production environment was changed.

## 2026-09-23 verification refresh

- Runtime head remains `a2ea61af4afbfe5a2b216ab998fbb93fc06e3707`; no new P0/P1 was found in the inspected target/delay/remote-user planner boundary.
- GitHub Quality run `35700160969`: **SUCCESS** — py_compile and 5/5 tests PASS.
- The repository still only prints reviewed commands; it never executes shutdown/restart, firewall, registry or remote-service actions.
- No canonical Vercel project is expected for this CLI/documentation product.

Status remains **PARTIAL** only for broader platform/manual command review. Keep Draft; no device action or merge.
