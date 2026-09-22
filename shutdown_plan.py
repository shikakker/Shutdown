#!/usr/bin/env python3
"""Generate a reviewed shutdown/restart plan without executing it."""

from __future__ import annotations

import argparse
import ipaddress
import math
import re
import shlex
from dataclasses import dataclass

SAFE_HOST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]{0,252}$")
SAFE_USER_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
MIN_DELAY_SECONDS = 60
MAX_DELAY_SECONDS = 86_400


@dataclass(frozen=True)
class ShutdownPlan:
    platform: str
    action: str
    target: str
    delay_seconds: int
    command: str
    abort_command: str
    warning: str


def validate_target(value: str) -> str:
    target = value.strip()
    if target == "local":
        return target

    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        pass

    if not SAFE_HOST_RE.fullmatch(target) or ".." in target:
        raise ValueError("Target must be 'local', a valid IP address, or a simple DNS hostname.")
    return target


def validate_delay(value: int) -> int:
    if value < MIN_DELAY_SECONDS or value > MAX_DELAY_SECONDS:
        raise ValueError(
            f"Delay must be between {MIN_DELAY_SECONDS} and {MAX_DELAY_SECONDS} seconds."
        )
    return value


def build_windows_plan(action: str, target: str, delay_seconds: int) -> ShutdownPlan:
    mode = "/s" if action == "shutdown" else "/r"
    remote = "" if target == "local" else f" /m \\{target}"
    command = (
        f'shutdown {mode} /t {delay_seconds}{remote} '
        '/c "Planned maintenance - save your work"'
    )
    abort = "shutdown /a" if target == "local" else f"shutdown /a /m \\{target}"
    return ShutdownPlan(
        platform="windows",
        action=action,
        target=target,
        delay_seconds=delay_seconds,
        command=command,
        abort_command=abort,
        warning="Review authorization, active users, backups and maintenance window before execution.",
    )


def build_linux_plan(
    action: str,
    target: str,
    delay_seconds: int,
    ssh_user: str | None,
) -> ShutdownPlan:
    minutes = max(1, math.ceil(delay_seconds / 60))
    mode = "-h" if action == "shutdown" else "-r"
    shutdown_command = f"sudo shutdown {mode} +{minutes}"
    abort_command = "sudo shutdown -c"

    if target != "local":
        if not ssh_user or not SAFE_USER_RE.fullmatch(ssh_user):
            raise ValueError("Remote Linux plans require a simple --ssh-user value.")
        host = f"{ssh_user}@{target}"
        shutdown_command = f"ssh {shlex.quote(host)} -- {shutdown_command}"
        abort_command = f"ssh {shlex.quote(host)} -- {abort_command}"

    return ShutdownPlan(
        platform="linux",
        action=action,
        target=target,
        delay_seconds=delay_seconds,
        command=shutdown_command,
        abort_command=abort_command,
        warning="Review authorization, active users, backups and maintenance window before execution.",
    )


def create_plan(
    platform: str,
    action: str,
    target: str,
    delay_seconds: int,
    ssh_user: str | None = None,
) -> ShutdownPlan:
    target = validate_target(target)
    delay_seconds = validate_delay(delay_seconds)

    if platform == "windows":
        return build_windows_plan(action, target, delay_seconds)
    if platform == "linux":
        return build_linux_plan(action, target, delay_seconds, ssh_user)
    raise ValueError("Unsupported platform.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a shutdown/restart plan. This tool never executes commands."
    )
    parser.add_argument("--platform", choices=("windows", "linux"), required=True)
    parser.add_argument("--action", choices=("shutdown", "restart"), default="shutdown")
    parser.add_argument("--target", default="local")
    parser.add_argument("--delay", type=int, default=300, help="Delay in seconds (60-86400).")
    parser.add_argument("--ssh-user", help="Required for remote Linux plans.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        plan = create_plan(
            platform=args.platform,
            action=args.action,
            target=args.target,
            delay_seconds=args.delay,
            ssh_user=args.ssh_user,
        )
    except ValueError as error:
        print(f"ERROR: {error}")
        return 2

    print("DRY RUN ONLY - no command was executed")
    print(f"Platform: {plan.platform}")
    print(f"Action: {plan.action}")
    print(f"Target: {plan.target}")
    print(f"Delay: {plan.delay_seconds} seconds")
    print(f"Planned command: {plan.command}")
    print(f"Abort command: {plan.abort_command}")
    print(f"Safety check: {plan.warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
