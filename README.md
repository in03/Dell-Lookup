# Dell-Lookup

A client and modular CLI app for Dell's Warranty API to retrieve asset info, perform bulk lookups and more.

> [!Warning] 🚧 This code is WIP and proof-of-concept. Use with caution.

## Features

- Fetch warranty information for Dell devices using Service Tags
- Bulk processing of CSV files containing Service Tag data
- Retrieve detailed asset information including:
  - Model information
  - Warranty start dates
  - Asset summaries
  - Warranty details

## Installation

Requires Python 3.12.8 or higher. Install dependencies using [uv](https://github.com/astral-sh/uv):

```shell
uv sync
```

## Configuration

The tool uses a TOML configuration file located in your system's application directory. To get started:

1. View the current configuration:
```shell
delly config show
```

2. Edit the configuration file:
```shell
delly config edit
```

The configuration file should contain your Dell API credentials:

```toml
[dell]
client_id = "your_client_id"
client_secret = "your_client_secret"
```

Other available configuration commands:
```shell
delly config browse  # Open config directory in file browser
delly config reset   # Reset to default values
delly config backup  # Create a backup of current config
```

## Usage

If you want to use the built in commands, you can use them

Install the tool with UV:
```shell
uv tool install --from git+https://github.com/in03/dell-lookup.git dell-lookup
```

1. Quick service tag lookup:
```shell
delly info SERVICE_TAG
```

2. Process a single CSV file:
```shell
delly bulk path/to/file.csv
```

3. Process all CSV files in a directory:
```shell
delly bulk --dir path/to/directory
```

4. Process all CSV files in the current directory:
```shell
delly bulk
```

This will prompt for a Service Tag and display detailed warranty information in a formatted table.

### Bulk Processing

The `bulk-model-add.py` script processes CSV files containing Dell Service Tags:

1. Place your CSV file(s) in the working directory
2. Run:

```shell
python scripts/bulk-model-add.py
```


#### CSV Format Requirements
Input CSV must have the following columns:

```csv
Service Tag,PKID,Express Service Code,Serial Number
```

The script will:
- Add "Model" and "Warranty Start" columns
- Create a new file with "_updated" suffix
- Process up to 100 service tags per API call

## API Client

The package includes a `DellWarrantyClient` class that handles:
- OAuth2 authentication
- Rate limiting
- API endpoint interactions

Available methods:
- `get_asset_header()`: Basic asset information
- `get_asset_warranty()`: Warranty details
- `get_asset_details()`: Detailed component information
- `get_asset_summary()`: Asset entitlement summary

## Dependencies

- httpx: Modern HTTP client
- pandas: Data processing
- pydantic: Data validation
- python-dotenv: Environment management
- rich: Terminal formatting

## Notes

- API is rate-limited to 100 service tags per request
- Warranty dates are formatted for Snipe-IT compatibility
- All API responses are cached to minimize API calls

## Usage

### Using the Client

You can use the client in your own scripts.

Add it to your Python environment:
```shell
# uv or pip or whatever you like
pip install git+https://github.com/in03/dell-lookup
```

Then import the client:
```python
from dell_lookup.client import DellWarrantyClient
```

### Using the CLI

You can access the [built-in scripts](/scripts/) through the CLI.

Install the tool with UV:
```shell
uv tool install --from git+https://github.com/in03/dell-lookup.git dell-lookup
```

1. Quick service tag lookup:
```shell
delly info SERVICE_TAG
```

2. Process a single CSV file:
```shell
delly bulk path/to/file.csv
```

3. Process all CSV files in a directory:
```shell
delly bulk --dir path/to/directory
```

4. Process all CSV files in the current directory:
```shell
delly bulk
```

### Extending the CLI

You can also fork this repo and add your own scripts:

1. Create a new script in the `scripts` directory
2. Make sure it has modular functions that can be imported
3. Add a new command to `src/dell_lookup/cli.py` using the `@app.command()` decorator
4. The CLI will automatically find and import your script functions

Push your changes and install on end devices like so:

```shell
uv tool install --from git+https://github.com/myusername/myrepo.git dell-lookup
```

The tool will be added to path, where you can call it like this:

```shell
delly mycustomscript SERVICE_TAG
```

