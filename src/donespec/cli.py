from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from donespec import __version__
from donespec.engine import validate_payload
from donespec.exceptions import SpecValidationError
from donespec.loader import load_spec
from donespec.output import error_to_json, print_human_report, report_to_json

app = typer.Typer(
    name="donespec",
    help="Deterministic validation for AI agent task completion.",
    no_args_is_help=True,
)
console = Console(stderr=False)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"donespec {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", callback=_version_callback, help="Show version and exit."),
    ] = False,
) -> None:
    _ = version


@app.command()
def validate(
    spec: Annotated[Path, typer.Argument(help="Path to done.json")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output."),
    ] = False,
    root: Annotated[
        Path | None,
        typer.Option("--root", help="Project root. Defaults to the spec file directory."),
    ] = None,
    fail_fast: Annotated[
        bool,
        typer.Option("--fail-fast", help="Stop after the first failed check."),
    ] = False,
) -> None:
    """Validate a DoneSpec task file."""
    spec_path = spec.resolve()
    root_dir = root.resolve() if root else spec_path.parent.resolve()

    try:
        payload = load_spec(spec_path)
        report = validate_payload(
            payload,
            spec_path=spec_path,
            root_dir=root_dir,
            fail_fast=fail_fast,
        )
    except SpecValidationError as exc:
        if json_output:
            sys.stdout.write(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Spec error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc
    except Exception as exc:
        if json_output:
            sys.stdout.write(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Runtime error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc

    if json_output:
        sys.stdout.write(report_to_json(report) + "\n")
    else:
        print_human_report(report, console=console)

    raise typer.Exit(code=report.exit_code)
