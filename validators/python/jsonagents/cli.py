"""Command-line interface for JSON Agents validator."""

import json
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from .validator import validate_manifest, ValidationResult


console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="jsonagents")
def main() -> None:
    """JSON Agents validator - validate Portable Agent Manifests."""
    pass


@main.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    "--strict",
    is_flag=True,
    help="Treat warnings as errors",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed validation output",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output results as JSON",
)
@click.option(
    "--schema",
    type=click.Path(exists=True),
    help="Path to custom json-agents.json schema",
)
def validate(
    files: tuple,
    strict: bool,
    verbose: bool,
    output_json: bool,
    schema: Optional[str],
) -> None:
    """
    Validate JSON Agents manifest files.

    Examples:
        jsonagents validate manifest.json
        jsonagents validate examples/*.json
        jsonagents validate manifest.json --strict --verbose
    """
    results: List[tuple[str, ValidationResult]] = []
    
    # Expand directories
    file_paths: List[Path] = []
    for file in files:
        path = Path(file)
        if path.is_dir():
            file_paths.extend(path.glob("*.json"))
        else:
            file_paths.append(path)

    if not file_paths:
        console.print("[yellow]No manifest files found[/yellow]")
        sys.exit(1)

    # Validate each file
    for file_path in file_paths:
        try:
            result = validate_manifest(file_path, strict=strict, schema_path=schema)
            results.append((str(file_path), result))
        except Exception as e:
            console.print(f"[red]Error validating {file_path}: {e}[/red]")
            results.append((str(file_path), ValidationResult(is_valid=False, errors=[str(e)])))

    # Output results
    if output_json:
        _output_json(results)
    else:
        _output_rich(results, verbose=verbose)

    # Exit with error code if any validation failed
    if any(not result.is_valid for _, result in results):
        sys.exit(1)


def _output_json(results: List[tuple[str, ValidationResult]]) -> None:
    """Output results as JSON."""
    output = []
    for file_path, result in results:
        output.append({
            "file": file_path,
            "valid": result.is_valid,
            "errors": result.errors,
            "warnings": result.warnings,
        })
    
    console.print(json.dumps(output, indent=2))


def _output_rich(results: List[tuple[str, ValidationResult]], verbose: bool) -> None:
    """Output results with rich formatting."""
    total = len(results)
    passed = sum(1 for _, r in results if r.is_valid)
    failed = total - passed

    # Show results for each file
    for file_path, result in results:
        if result.is_valid:
            icon = "✅"
            color = "green"
            status = "VALID"
        else:
            icon = "❌"
            color = "red"
            status = "INVALID"

        console.print(f"\n{icon} [bold]{file_path}[/bold] - [{color}]{status}[/{color}]")

        if result.errors:
            console.print("\n[red bold]Errors:[/red bold]")
            for error in result.errors:
                console.print(f"  [red]•[/red] {error}")

        if result.warnings:
            console.print("\n[yellow bold]Warnings:[/yellow bold]")
            for warning in result.warnings:
                console.print(f"  [yellow]•[/yellow] {warning}")

        # Show manifest snippet in verbose mode
        if verbose and result.manifest:
            console.print("\n[dim]Manifest preview:[/dim]")
            preview = json.dumps(result.manifest, indent=2)[:500]
            if len(json.dumps(result.manifest)) > 500:
                preview += "\n..."
            syntax = Syntax(preview, "json", theme="monokai", line_numbers=False)
            console.print(syntax)

    # Summary table
    console.print()
    table = Table(title="Validation Summary", show_header=True, header_style="bold")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right")
    
    table.add_row("Total Files", str(total))
    table.add_row("Passed", f"[green]{passed}[/green]")
    table.add_row("Failed", f"[red]{failed}[/red]" if failed > 0 else "0")
    
    console.print(table)

    # Final status
    if failed == 0:
        console.print("\n[green bold]✅ All manifests are valid![/green bold]")
    else:
        console.print(f"\n[red bold]❌ {failed} manifest(s) failed validation[/red bold]")


@main.command()
@click.argument("uri")
def check_uri(uri: str) -> None:
    """
    Validate an ajson:// URI.

    Example:
        jsonagents check-uri ajson://example.com/agents/hello
    """
    from .uri import URIValidator

    validator = URIValidator()
    result = validator.validate(uri)

    if result.is_valid:
        console.print(f"[green]✅ Valid URI:[/green] {uri}")
        
        # Show parsed components
        console.print("\n[bold]Parsed Components:[/bold]")
        for key, value in result.parsed.items():
            if value:
                console.print(f"  {key}: {value}")
        
        # Show HTTPS transformation
        try:
            https_url = validator.to_https(uri)
            console.print(f"\n[bold]HTTPS URL:[/bold] {https_url}")
        except Exception as e:
            console.print(f"\n[yellow]Could not transform to HTTPS: {e}[/yellow]")
    else:
        console.print(f"[red]❌ Invalid URI:[/red] {uri}")
        for error in result.errors:
            console.print(f"  [red]•[/red] {error}")
    
    if result.warnings:
        console.print("\n[yellow bold]Warnings:[/yellow bold]")
        for warning in result.warnings:
            console.print(f"  [yellow]•[/yellow] {warning}")

    sys.exit(0 if result.is_valid else 1)


@main.command()
@click.argument("expression")
def check_policy(expression: str) -> None:
    """
    Validate a policy where clause expression.

    Example:
        jsonagents check-policy "tool.type == 'http' && tool.auth.method != 'none'"
    """
    from .policy import PolicyValidator

    validator = PolicyValidator()
    result = validator.validate(expression)

    if result.is_valid:
        console.print(f"[green]✅ Valid expression[/green]")
        console.print(f"\n[dim]{expression}[/dim]")
    else:
        console.print(f"[red]❌ Invalid expression[/red]")
        console.print(f"\n[dim]{expression}[/dim]")
        console.print("\n[red bold]Errors:[/red bold]")
        for error in result.errors:
            console.print(f"  [red]•[/red] {error}")
    
    if result.warnings:
        console.print("\n[yellow bold]Warnings:[/yellow bold]")
        for warning in result.warnings:
            console.print(f"  [yellow]•[/yellow] {warning}")

    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
