import os
import pandas as pd
from dotenv import load_dotenv
from dell_lookup.client import DellWarrantyClient
from rich.console import Console
from rich.logging import RichHandler
from rich import print
import logging
from datetime import datetime
from rich.table import Table

# Initialize console and logging
console = Console()
logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[RichHandler()])
logger = logging.getLogger("rich")

def get_warranty_info(service_tag: str) -> Table:
    """
    Fetch and format warranty information for a given service tag.
    
    Args:
        service_tag (str): The Dell service tag to look up
        
    Returns:
        rich.table.Table: A formatted table containing the warranty information
    """
    load_dotenv()
    
    service_tag = service_tag.upper()
    logger.info(f"Fetching information for Service Tag: {service_tag}")

    # Initialize the DellWarrantyClient
    client = DellWarrantyClient(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))

    # Fetch asset header
    asset_header = client.get_asset_header([service_tag])
    asset_summary = client.get_asset_summary([service_tag])

    if not asset_header:
        logger.warning(f"No information found for Service Tag: {service_tag}")
        return None

    # Create a rich table to display the information
    table = Table(title="Warranty Information")

    # Add columns to the table
    table.add_column("Field", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="left", style="magenta")

    # Extract and add data to the table
    header = asset_header[0]
    table.add_row("Service Tag", service_tag)
    table.add_row("Model", header.get("productLineDescription", "Unknown"))
    
    ship_date_str = header.get("shipDate")
    if ship_date_str:
        ship_date = datetime.strptime(ship_date_str, '%Y-%m-%dT%H:%M:%SZ')
        table.add_row("Warranty Start", ship_date.strftime("%Y-%m-%d"))
    else:
        table.add_row("Warranty Start", "Unknown")

    return table

def main():
    """CLI entrypoint when script is run directly."""
    service_tag_input = input("Enter the Service Tag: ")
    table = get_warranty_info(service_tag_input)
    if table:
        console.print(table)

if __name__ == "__main__":
    main()
