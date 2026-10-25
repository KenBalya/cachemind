"""Automated tests for the CacheMind command-line interface."""

import subprocess

import pytest

from cachemind import cli


def test_cli_displays_help_without_arguments(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should display help when no command is provided."""

    exit_code = cli.main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "usage: cachemind" in captured.out
    assert "doctor" in captured.out


def test_cli_help_option(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The help option should terminate successfully."""

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "Autonomous Workload-Aware" in captured.out


def test_cli_version(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The version option should report the installed version."""

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "cachemind 0.1.0" in captured.out


def test_cli_rejects_unknown_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An unknown command must produce a usage error."""

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["nonexistent"])

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "invalid choice" in captured.err


def test_doctor_detects_missing_tools(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The doctor must fail when required tools are unavailable."""

    monkeypatch.setattr(
        cli.shutil,
        "which",
        lambda executable: None,
    )

    exit_code = cli.main(["doctor"])

    captured = capsys.readouterr()

    assert exit_code == 1

    assert "[MISSING] Git" in captured.out
    assert "[MISSING] GCC" in captured.out
    assert "[MISSING] CMake" in captured.out
    assert "[MISSING] Ninja" in captured.out
    assert "[MISSING] CTest" in captured.out


def test_doctor_accepts_valid_environment(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The doctor must succeed when all requirements are satisfied."""

    def fake_which(executable: str) -> str:
        return f"C:/msys64/ucrt64/bin/{executable}.exe"

    monkeypatch.setattr(
        cli.shutil,
        "which",
        fake_which,
    )

    monkeypatch.setattr(
        cli,
        "check_compiler",
        lambda compiler_path: True,
    )

    monkeypatch.setattr(
        cli.platform,
        "system",
        lambda: "Windows",
    )

    monkeypatch.setattr(
        cli.platform,
        "machine",
        lambda: "AMD64",
    )

    exit_code = cli.main(["doctor"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Environment validation: PASSED" in captured.out


def test_compiler_validation_accepts_ucrt64(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A valid MSYS2 UCRT64 compiler should be accepted."""

    def fake_run(args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="x86_64-w64-mingw32\n",
            stderr="",
        )

    monkeypatch.setattr(
        cli.subprocess,
        "run",
        fake_run,
    )

    result = cli.check_compiler("C:/msys64/ucrt64/bin/g++.exe")

    assert result is True


def test_compiler_validation_rejects_wrong_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A compiler targeting another architecture must be rejected."""

    def fake_run(args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="aarch64-linux-gnu\n",
            stderr="",
        )

    monkeypatch.setattr(
        cli.subprocess,
        "run",
        fake_run,
    )

    result = cli.check_compiler("C:/msys64/ucrt64/bin/g++.exe")

    assert result is False
