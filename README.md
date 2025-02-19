# Dell-Lookup

A Python package for interacting with Dell's Warranty API to retrieve asset information and perform bulk lookups.

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

Requires Python 3.12.8 or higher. Install dependencies using:

```shell
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory
2. Add your Dell API credentials:

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```


## Usage

### Quick Single Lookup

Use the `get-extended-info.py` script for quick individual Service Tag lookups:

```shell
python scripts/get-extended-info.py
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

```
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

## Contributing

This is a work in progress. Contributions and improvements are welcome!
