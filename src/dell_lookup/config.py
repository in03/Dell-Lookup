"""
Configuration management for Dell-Lookup.
"""
from pathlib import Path
import tomli
import tomli_w
from typing import Dict, Optional
import typer
from rich import print
import os
import shutil
import subprocess

# Get the user's config directory based on platform
CONFIG_DIR = Path(typer.get_app_dir("dell-lookup"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "dell": {
        "client_id": "",
        "client_secret": "",
    }
}

def ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict:
    """Load the configuration file."""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "rb") as f:
            return tomli.load(f)
    except Exception as e:
        print(f"[red]Error loading config: {e}[/red]")
        return DEFAULT_CONFIG

def save_config(config: Dict) -> None:
    """Save the configuration to file."""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(config, f)
    except Exception as e:
        print(f"[red]Error saving config: {e}[/red]")
        raise

def show_config() -> None:
    """Display the current configuration."""
    config = load_config()
    
    # Mask sensitive values
    if "dell" in config:
        if config["dell"].get("client_id"):
            config["dell"]["client_id"] = "****" + config["dell"]["client_id"][-4:]
        if config["dell"].get("client_secret"):
            config["dell"]["client_secret"] = "****" + config["dell"]["client_secret"][-4:]
    
    print("\n[bold]Current Configuration:[/bold]")
    print(tomli_w.dumps(config))

def edit_config() -> None:
    """Open the config file in the default editor."""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    
    editor = os.environ.get("EDITOR", "vim")
    try:
        subprocess.run([editor, str(CONFIG_FILE)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[red]Error opening editor: {e}[/red]")
    except FileNotFoundError:
        print(f"[red]Editor '{editor}' not found. Set the EDITOR environment variable to your preferred editor.[/red]")

def reset_config() -> None:
    """Reset the configuration to default values."""
    save_config(DEFAULT_CONFIG)
    print("[green]Configuration reset to defaults.[/green]")

def backup_config() -> Optional[Path]:
    """Create a backup of the current config file."""
    if not CONFIG_FILE.exists():
        print("[yellow]No configuration file exists to backup.[/yellow]")
        return None
    
    backup_file = CONFIG_FILE.with_suffix(".toml.backup")
    try:
        shutil.copy2(CONFIG_FILE, backup_file)
        print(f"[green]Backup created: {backup_file}[/green]")
        return backup_file
    except Exception as e:
        print(f"[red]Error creating backup: {e}[/red]")
        return None

def browse_config() -> None:
    """Open the config directory in the system file browser."""
    ensure_config_dir()
    
    try:
        if os.name == "nt":  # Windows
            os.startfile(CONFIG_DIR)
        elif os.name == "posix":  # macOS and Linux
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(CONFIG_DIR)], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(CONFIG_DIR)], check=True)
    except Exception as e:
        print(f"[red]Error opening file browser: {e}[/red]") 