from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from donespec import __version__
from donespec.engine import validate_payload
from donespec.exceptions import SpecValidationError
from donespec.init_project import AgentMode, initialize_project
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


@app.command(name="init")
def init_command(
    root: Annotated[
        Path,
        typer.Argument(help="Project root to initialize."),
    ] = Path("."),
    agent: Annotated[
        AgentMode,
        typer.Option(
            "--agent",
            case_sensitive=False,
            help="Agent instruction mode: all, codex, claude, or none.",
        ),
    ] = AgentMode.all,
    with_vscode: Annotated[
        bool,
        typer.Option(
            "--with-vscode/--no-vscode",
            help="Create VS Code tasks.",
        ),
    ] = True,
    with_hooks: Annotated[
        bool,
        typer.Option(
            "--with-hooks/--no-hooks",
            help="Create Git hook files and installers.",
        ),
    ] = True,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Overwrite existing DoneSpec files.",
        ),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Run non-interactively with defaults.",
        ),
    ] = False,
) -> None:
    """Initialize DoneSpec files in a project."""
    _ = yes

    result = initialize_project(
        root,
        agent=agent,
        with_vscode=with_vscode,
        with_hooks=with_hooks,
        force=force,
    )

    console.print("[bold green]DoneSpec project initialized.[/bold green]")

    if result.created:
        console.print("\n[bold]Created:[/bold]")
        for path in result.created:
            console.print(f"✓ {path}")

    if result.overwritten:
        console.print("\n[bold yellow]Overwritten:[/bold yellow]")
        for path in result.overwritten:
            console.print(f"↻ {path}")

    if result.skipped:
        console.print("\n[bold]Skipped existing files:[/bold]")
        for path in result.skipped:
            console.print(f"- {path}")

    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Review done.json")
    console.print("2. Run: donespec validate done.json")

    if with_hooks:
        console.print("3. Optional: install Git hooks")
        console.print("   Windows: .\\scripts\\install-git-hooks.ps1")
        console.print("   Unix:    ./scripts/install-git-hooks.sh")
