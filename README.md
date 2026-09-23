# Shutdown Planner

This repository is a **safe planning/reference utility** for authorized system maintenance. It does **not** remotely execute shutdowns and it does not enable remote administration services.

The original notes contained immediate shutdown examples (`/t 0`, `shutdown now`) and force-close guidance. Those examples have been replaced with a dry-run planner that validates the target, requires a delay of at least 60 seconds, omits force-close flags, and always prints an abort command.

## Usage

Generate a local Windows maintenance plan:

```bash
python shutdown_plan.py --platform windows --action shutdown --target local --delay 300
```

Generate a remote Windows plan:

```bash
python shutdown_plan.py --platform windows --action restart --target workstation-12.example --delay 600
```

Generate a remote Linux plan:

```bash
python shutdown_plan.py --platform linux --action shutdown --target 10.0.0.25 --ssh-user admin --delay 300
```

The tool prints the planned command and its abort command. **It never invokes either command.**

## Safety boundary

Before an operator manually executes a generated command, verify:

- explicit authorization for the target system;
- the target identity and maintenance window;
- active-user impact and data-save/backup state;
- a tested recovery path and the printed abort command;
- least-privilege remote administration already configured by the organization.

This project intentionally does not open firewall ports, enable Remote Registry/SSH, store credentials, bypass confirmation, force-close applications, or provide an unauthenticated remote-control service.

## Verification

```bash
python -m unittest discover -s tests -v
```

No production shutdown, restart, remote service mutation, credential change or firewall change is performed by this repository.
