import os
import pandas as pd
from dotenv import load_dotenv
from dell_lookup.client import DellWarrantyClient
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress
from rich import print
import logging
from datetime import datetime

load_dotenv()

# Initialize console and logging
console = Console()
logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[RichHandler()])
logger = logging.getLogger("rich")

# Set INPUT_DIR to the current working directory
INPUT_DIR = os.getcwd()

# Function to process a single CSV file
def process_csv(file_path):
    logger.info(f"Processing file: {file_path}")
    df = pd.read_csv(file_path)
    if "Service Tag" not in df.columns:
        logger.warning(f"Skipping file {file_path}: No 'Service Tag' column found.")
        return

    # Initialize the DellWarrantyClient
    client = DellWarrantyClient(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))

    # Add new columns
    models = []
    warranties = []

    # Fetch model and warranty information using the client
    service_tags = df["Service Tag"].tolist()
    asset_headers = []

    logger.info("Fetching asset headers...")
    asset_headers = client.get_asset_header(service_tags)  # Fetch asset headers

    # print(asset_headers)

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
    file_name, file_extension = os.path.splitext(file_path)
    new_file_path = f"{file_name}_updated{file_extension}"
    df.to_csv(new_file_path, index=False)
    logger.info(f"File updated: {new_file_path}")

# Main processing loop
if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        logger.error(f"Input directory '{INPUT_DIR}' does not exist.")
        exit(1)

    input_files = [
        os.path.join(INPUT_DIR, file)
        for file in os.listdir(INPUT_DIR)
        if file.endswith(".csv")
    ]

    if not input_files:
        logger.error(f"No CSV files found in directory '{INPUT_DIR}'.")
        exit(1)

    # Use progress bar for total number of CSVs processed
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing CSV files...", total=len(input_files))
        for file_path in input_files:
            process_csv(file_path)
            progress.update(task, advance=1)

    logger.info("Processing complete.")
