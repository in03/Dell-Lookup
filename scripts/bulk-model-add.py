import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from dell_lookup.client import DellWarrantyClient
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress
from rich import print
import logging
from datetime import datetime
from typing import List, Optional

# Initialize console and logging
console = Console()
logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[RichHandler()])
logger = logging.getLogger("rich")

def process_csv(file_path: Path) -> Optional[Path]:
    """
    Process a CSV file containing Dell service tags and add model/warranty information.
    
    Args:
        file_path (Path): Path to the CSV file to process
        
    Returns:
        Optional[Path]: Path to the updated CSV file, or None if processing failed
    """
    load_dotenv()
    logger.info(f"Processing file: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        return None
        
    if "Service Tag" not in df.columns:
        logger.warning(f"Skipping file {file_path}: No 'Service Tag' column found.")
        return None

    # Initialize the DellWarrantyClient
    client = DellWarrantyClient(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))

    # Add new columns
    models = []
    warranties = []

    # Fetch model and warranty information using the client
    service_tags = df["Service Tag"].tolist()
    
    logger.info("Fetching asset headers...")
    asset_headers = client.get_asset_header(service_tags)

    for header in asset_headers:
        # Get model
        models.append(header.get("productLineDescription", "Unknown"))

        # Get warranty start
        ship_date_str = header.get("shipDate")
        if ship_date_str:
            # Parse the string to a datetime object
            ship_date = datetime.strptime(ship_date_str, '%Y-%m-%dT%H:%M:%SZ')
            warranties.append(ship_date.strftime("%Y-%m-%d")) #? SNIPE friendly
        else:
            warranties.append("Unknown")

    df["Model"] = models
    df["Warranty Start"] = warranties

    # Save the updated CSV with an incremental suffix
    new_file_path = file_path.parent / f"{file_path.stem}_updated{file_path.suffix}"
    df.to_csv(new_file_path, index=False)
    logger.info(f"File updated: {new_file_path}")
    return new_file_path

def process_directory(directory: Path = None) -> List[Path]:
    """
    Process all CSV files in a directory.
    
    Args:
        directory (Path, optional): Directory to process. Defaults to current directory.
        
    Returns:
        List[Path]: List of paths to updated CSV files
    """
    if directory is None:
        directory = Path.cwd()
    
    if not directory.exists():
        logger.error(f"Input directory '{directory}' does not exist.")
        return []

    input_files = list(directory.glob("*.csv"))

    if not input_files:
        logger.error(f"No CSV files found in directory '{directory}'.")
        return []

    updated_files = []
    
    # Use progress bar for total number of CSVs processed
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing CSV files...", total=len(input_files))
        for file_path in input_files:
            if updated_file := process_csv(file_path):
                updated_files.append(updated_file)
            progress.update(task, advance=1)

    logger.info("Processing complete.")
    return updated_files

def main():
    """CLI entrypoint when script is run directly."""
    process_directory()

if __name__ == "__main__":
    main()
