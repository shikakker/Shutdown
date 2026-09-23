# Shutdown — Safety & Modernization Roadmap

The repository is currently a documentation/demo project describing local and remote shutdown techniques for Windows, Python and Bash. It should be treated as an administrative scripting reference, not as a remote-management product.

## 10 tasks
1. Add a prominent authorization boundary: remote shutdown commands are for systems you own or administer with permission.
2. Separate Windows local shutdown, Windows remote RPC shutdown and Linux SSH shutdown into distinct documented workflows.
3. Replace hard-coded IP examples with placeholders and avoid examples that imply blind execution against arbitrary hosts.
4. Add preflight checks for target reachability, privileges and required services before any future automation script executes a shutdown.
5. Add an explicit confirmation/dry-run mode to any executable wrapper built from these examples.
6. Document rollback/recovery expectations, including how to cancel delayed shutdowns where supported.
7. Prefer secure SSH key handling and least-privilege administration rather than password embedding or broad remote-admin enablement.
8. Add tests for argument construction and validation if Python/Bash wrappers are added; do not test destructive shutdowns in CI.
9. Add platform/version notes so commands are not presented as universally portable across Windows/Linux environments.
10. Position the repository as a systems-administration scripting reference or learning artifact, not as security tooling or remote-device management infrastructure.

## Portfolio value
Low as a standalone product case, but useful supporting evidence of systems/automation familiarity when framed responsibly.