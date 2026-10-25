"""CacheMind command-line interface."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys

from collections.abc import Sequence
from importlib.metadata import version
from pathlib import Path


REQUIRED_TOOLS = {
    "uv": "uv",
    "Git": "git",
    "GCC": "g++",
    "CMake": "cmake",
    "Ninja": "ninja",
    "CTest": "ctest",
}

EXPECTED_GCC_TARGET = "x86_64-w64-mingw32"


def check_compiler(compiler_path: str) -> bool:
    """
    Verify that GCC targets native Windows x64.

    Returns:
        True if the compiler target is supported.
        False otherwise.
    """

    try:
        result = subprocess.run(
            [compiler_path, "-dumpmachine"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"[FAIL] Unable to inspect GCC: {error}")
        return False

    if result.returncode != 0:
        print("[FAIL] GCC architecture inspection failed.")
        return False

    target = result.stdout.strip()

    print(f"GCC target: {target}")

    if target != EXPECTED_GCC_TARGET:
        print(
            "[FAIL] Expected Windows x64 GCC target: "
            f"{EXPECTED_GCC_TARGET}"
        )
        return False

    compiler_parts = {
        part.lower()
        for part in Path(compiler_path).parts
    }

    if "ucrt64" not in compiler_parts:
        print(
            "[FAIL] GCC must come from the "
            "MSYS2 UCRT64 toolchain."
        )
        return False

    return True


def doctor() -> int:
    """
    Validate the CacheMind development environment.

    Returns:
        0 when all checks pass.
        1 when at least one check fails.
    """

    print("=" * 60)
    print("CacheMind Development Environment")
    print("=" * 60)

    print(f"Python: {platform.python_version()}")
    print(f"Executable: {sys.executable}")
    print(f"Operating System: {platform.system()}")
    print(f"Architecture: {platform.machine()}")
    print()

    errors: list[str] = []

    # --------------------------------------------------
    # Python compatibility
    # --------------------------------------------------

    if sys.version_info[:2] == (3, 12):
        print("[OK] Python 3.12")

    else:
        print("[FAIL] Python 3.12 required.")
        errors.append("Unsupported Python version.")

    # --------------------------------------------------
    # Operating system compatibility
    # --------------------------------------------------

    if platform.system() == "Windows":
        print("[OK] Windows")

    else:
        print("[FAIL] Windows required.")
        errors.append("Unsupported operating system.")

    if platform.machine().lower() in {"amd64", "x86_64"}:
        print("[OK] x64 architecture")

    else:
        print("[FAIL] x64 architecture required.")
        errors.append("Unsupported system architecture.")

    # --------------------------------------------------
    # Development tools
    # --------------------------------------------------

    print()
    print("Development Tools")
    print("-" * 60)

    detected_tools: dict[str, str] = {}

    for name, executable in REQUIRED_TOOLS.items():
        executable_path = shutil.which(executable)

        if executable_path is None:
            print(f"[MISSING] {name}")
            errors.append(f"{name} not found.")

        else:
            print(f"[OK] {name}: {executable_path}")
            detected_tools[name] = executable_path

    # --------------------------------------------------
    # GCC verification
    # --------------------------------------------------

    gcc_path = detected_tools.get("GCC")

    if gcc_path is not None:
        print()
        print("Compiler Verification")
        print("-" * 60)

        if not check_compiler(gcc_path):
            errors.append("GCC verification failed.")

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    print()
    print("=" * 60)

    if errors:
        print("Environment validation: FAILED")

        for error in errors:
            print(f"- {error}")

        return 1

    print("Environment validation: PASSED")

    return 0


def build_parser() -> argparse.ArgumentParser:
    """
    Construct the CacheMind argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="cachemind",
        description=(
            "Autonomous Workload-Aware Cache Policy Optimizer"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('cachemind')}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available Commands",
    )

    subparsers.add_parser(
        "doctor",
        help="Validate the CacheMind development environment.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """
    Execute the CacheMind CLI.

    Args:
        argv:
            Optional argument sequence.
            If None, argparse reads sys.argv.

    Returns:
        Process exit code.
    """

    parser = build_parser()

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return doctor()

    parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())