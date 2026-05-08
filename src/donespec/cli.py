from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from donespec import __version__
from donespec.doctor import DoctorReport, run_doctor
from donespec.engine import validate_payload
from donespec.exceptions import SpecValidationError
from donespec.explain import explain_payload, explain_to_text
from donespec.init_project import (
    AgentMode,
    TemplateMode,
    available_templates,
    initialize_project,
)
from donespec.loader import load_spec
from donespec.output import (
    error_to_json,
    print_human_report,
    report_to_json,
    safe_symbol_for_console,
    status_symbol_for_console,
    status_symbols_for_console,
    write_text,
)
from donespec.schema_command import get_schema_text, write_schema_file

app = typer.Typer(
    name="donespec",
    help="Deterministic completion validation for local development and CI.",
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
    strict: Annotated[
        bool,
        typer.Option("--strict", help="Enable strict semantic validation of done.json."),
    ] = False,
) -> None:
    """Validate a DoneSpec task file."""
    spec_path = spec.resolve()
    root_dir = root.resolve() if root else spec_path.parent.resolve()

    try:
        payload = load_spec(spec_path, strict=strict)
        report = validate_payload(
            payload,
            spec_path=spec_path,
            root_dir=root_dir,
            fail_fast=fail_fast,
        )
    except SpecValidationError as exc:
        if json_output:
            write_text(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Spec error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc
    except Exception as exc:
        if json_output:
            write_text(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Runtime error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc

    if json_output:
        write_text(report_to_json(report) + "\n")
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
    template: Annotated[
        TemplateMode,
        typer.Option(
            "--template",
            case_sensitive=False,
            help="Starter done.json template: generic, python, node, docs, or api.",
        ),
    ] = TemplateMode.generic,
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
        template=template,
        with_vscode=with_vscode,
        with_hooks=with_hooks,
        force=force,
    )

    console.print("[bold green]DoneSpec project initialized.[/bold green]")
    console.print(f"\nTemplate: [bold]{template.value}[/bold]")

    if result.created:
        console.print("\n[bold]Created:[/bold]")
        created_symbol, _ = status_symbols_for_console(console)
        for path in result.created:
            console.print(f"{created_symbol} {path}")

    if result.overwritten:
        console.print("\n[bold yellow]Overwritten:[/bold yellow]")
        overwritten_symbol = safe_symbol_for_console(console, "\u21bb", "*")
        for path in result.overwritten:
            console.print(f"{overwritten_symbol} {path}")

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


@app.command()
def explain(
    spec: Annotated[
        Path,
        typer.Argument(help="Path to done.json to explain."),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output."),
    ] = False,
    strict: Annotated[
        bool,
        typer.Option("--strict", help="Enable strict semantic validation before explaining."),
    ] = False,
) -> None:
    """Explain a DoneSpec task file without executing checks."""
    spec_path = spec.resolve()

    try:
        payload = load_spec(spec_path, strict=strict)
        explanation = explain_payload(payload, spec_path=spec_path)
    except SpecValidationError as exc:
        if json_output:
            write_text(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Spec error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc
    except Exception as exc:
        if json_output:
            write_text(error_to_json(str(exc)) + "\n")
        else:
            console.print(f"[bold red]Runtime error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc

    if json_output:
        write_text(json.dumps(explanation, indent=2) + "\n")
    else:
        write_text(explain_to_text(explanation))

    raise typer.Exit(code=0)


@app.command(name="add-check")
def add_check(
    spec: Annotated[
        Path,
        typer.Argument(help="Path to done.json to update."),
    ],
    check_type: Annotated[
        str,
        typer.Option("--type", help="Check type to add."),
    ],
    name: Annotated[
        str,
        typer.Option("--name", help="Unique check name."),
    ],
    group: Annotated[
        str,
        typer.Option("--group", help="Target group: must_pass or must_not."),
    ] = "must_pass",
    check_id: Annotated[
        str | None,
        typer.Option("--id", help="Optional unique check id."),
    ] = None,
    path: Annotated[
        str | None,
        typer.Option("--path", help="Path used by file and regex checks."),
    ] = None,
    pattern: Annotated[
        str | None,
        typer.Option("--pattern", help="Regex pattern used by regex checks."),
    ] = None,
    run: Annotated[
        str | None,
        typer.Option("--run", help="Command used by command checks."),
    ] = None,
    url: Annotated[
        str | None,
        typer.Option("--url", help="URL used by http_check checks."),
    ] = None,
    method: Annotated[
        str,
        typer.Option("--method", help="HTTP method used by http_check checks."),
    ] = "GET",
    expected_status: Annotated[
        int,
        typer.Option("--expected-status", help="Expected HTTP status for http_check."),
    ] = 200,
    expected_exit_code: Annotated[
        int,
        typer.Option("--expected-exit-code", help="Expected exit code for command checks."),
    ] = 0,
    timeout_seconds: Annotated[
        float | None,
        typer.Option("--timeout-seconds", help="Optional timeout in seconds."),
    ] = None,
    flags: Annotated[
        list[str] | None,
        typer.Option("--flag", help="Regex flag. Can be passed multiple times."),
    ] = None,
    headers_json: Annotated[
        str | None,
        typer.Option("--headers-json", help="HTTP headers as a JSON object."),
    ] = None,
) -> None:
    """Safely add a check to a DoneSpec contract."""
    from donespec.author import add_check_to_file

    try:
        result = add_check_to_file(
            spec,
            group=group,
            check_type=check_type,
            name=name,
            check_id=check_id,
            path=path,
            pattern=pattern,
            run=run,
            url=url,
            method=method,
            expected_status=expected_status,
            expected_exit_code=expected_exit_code,
            timeout_seconds=timeout_seconds,
            flags=flags,
            headers_json=headers_json,
        )
    except SpecValidationError as exc:
        console.print(f"[bold red]Spec error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc

    console.print("[bold green]DoneSpec check added.[/bold green]")
    console.print(f"Spec: {result.spec_path}")
    console.print(f"Group: {result.group}")
    console.print(f"Type: {result.check['type']}")
    console.print(f"Name: {result.check['name']}")


@app.command(name="schema")
def schema_command(
    write_path: Annotated[
        Path | None,
        typer.Option(
            "--write",
            help="Write the packaged DoneSpec JSON Schema to a file.",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Overwrite the target schema file when used with --write.",
        ),
    ] = False,
) -> None:
    """Print or write the DoneSpec JSON Schema."""
    if write_path is None:
        write_text(get_schema_text())
        raise typer.Exit(code=0)

    try:
        target = write_schema_file(write_path, force=force)
    except FileExistsError as exc:
        console.print(f"[bold red]Schema file already exists:[/bold red] {exc}")
        console.print("Use --force to overwrite it.")
        raise typer.Exit(code=1) from exc

    console.print("[bold green]DoneSpec schema written.[/bold green]")
    console.print(f"Path: {target}")


@app.command()
def templates(
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output."),
    ] = False,
) -> None:
    """List available DoneSpec init templates."""
    items = available_templates()

    if json_output:
        payload = {
            "templates": [{"name": item.name, "description": item.description} for item in items]
        }
        write_text(json.dumps(payload, indent=2) + "\n")
        raise typer.Exit(code=0)

    console.print("[bold]Available DoneSpec templates[/bold]\n")

    template_symbol, _ = status_symbols_for_console(console)
    for item in items:
        console.print(f"{template_symbol} [bold]{item.name}[/bold] - {item.description}")

    console.print("\nExample:")
    console.print("  donespec init --template python --yes")


@app.command()
def doctor(
    root: Annotated[
        Path,
        typer.Argument(help="Project root to inspect."),
    ] = Path("."),
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON output."),
    ] = False,
) -> None:
    """Inspect whether a project is DoneSpec-ready."""
    report = run_doctor(root)

    if json_output:
        write_text(json.dumps(report.to_dict(), indent=2) + "\n")
    else:
        _print_doctor_report(report)

    raise typer.Exit(code=0 if report.required_passed else 1)


def _print_doctor_report(report: DoctorReport) -> None:
    console.print("[bold]DoneSpec doctor[/bold]\n")
    console.print(f"Root: {report.root}\n")

    for check in report.checks:
        symbol = status_symbol_for_console(console, check.passed)
        style = "green" if check.passed else "red"
        required = " required" if check.required else ""
        details = f"  {check.details}" if check.details else ""

        console.print(f"[{style}]{symbol}[/{style}] {check.name}{required}{details}")

    if report.required_passed:
        console.print("\n[bold green]Project has the required DoneSpec files.[/bold green]")
    else:
        console.print("\n[bold red]Project is missing required DoneSpec files.[/bold red]")

    if report.all_passed:
        console.print("[bold green]Recommended integration is complete.[/bold green]")
    else:
        console.print("[yellow]Some optional integration checks are missing.[/yellow]")
