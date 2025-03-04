"""
Dell-Lookup CLI tool for interacting with Dell's Warranty API.
"""
from pathlib import Path
import sys
from typing import Optional
import typer
from rich.console import Console
from . import config

# Add the scripts directory to the Python path
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.append(str(SCRIPTS_DIR))

# Initialize Typer app and Rich console
app = typer.Typer(
    name="delly",
    help="Dell-Lookup CLI tool for interacting with Dell's Warranty API",
    add_completion=False,
)
console = Console()

# Create config command group
config_app = typer.Typer(help="Manage Dell-Lookup configuration")
app.add_typer(config_app, name="config")

@config_app.command("show")
def config_show():
    """Display the current configuration."""
    config.show_config()

@config_app.command("edit")
def config_edit():
    """Open the configuration file in your default editor."""
    config.edit_config()

@config_app.command("reset")
def config_reset():
    """Reset the configuration to default values."""
    config.reset_config()

@config_app.command("backup")
def config_backup():
    """Create a backup of the current configuration."""
    config.backup_config()

@config_app.command("browse")
def config_browse():
    """Open the configuration directory in your file browser."""
    config.browse_config()

@app.command()
def info(
    service_tag: str = typer.Argument(..., help="Service tag to look up"),
    extended: bool = typer.Option(False, "--extended", "-e", help="Show extended information"),
):
    """Get warranty information for a single service tag."""
    try:
        from get_extended_info import get_warranty_info
        table = get_warranty_info(service_tag)
        if table:
            console.print(table)
        else:
            raise typer.Exit(code=1)
    except ImportError as e:
        console.print(f"[red]Error: Could not load get-extended-info script: {e}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)

@app.command()
def bulk(
    csv_file: Optional[Path] = typer.Argument(
        None,
        help="CSV file containing service tags",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    directory: Path = typer.Option(
        None,
        "--dir", "-d",
        help="Directory containing CSV files to process",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
):
    """Process CSV files containing service tags and add model information."""
    try:
        from bulk_model_add import process_csv, process_directory
        
        if csv_file:
            # Process single file
            if updated_file := process_csv(csv_file):
                console.print(f"[green]Successfully processed: {updated_file}[/green]")
            else:
                console.print("[red]Failed to process CSV file[/red]")
                raise typer.Exit(code=1)
        elif directory:
            # Process directory
            updated_files = process_directory(directory)
            if updated_files:
                console.print("\n[green]Successfully processed files:[/green]")
                for file in updated_files:
                    console.print(f"  - {file}")
            else:
                console.print("[red]No files were processed successfully[/red]")
                raise typer.Exit(code=1)
        else:
            # Process current directory
            updated_files = process_directory()
            if updated_files:
                console.print("\n[green]Successfully processed files:[/green]")
                for file in updated_files:
                    console.print(f"  - {file}")
            else:
                console.print("[red]No files were processed successfully[/red]")
                raise typer.Exit(code=1)
                
    except ImportError as e:
        console.print(f"[red]Error: Could not load bulk-model-add script: {e}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 