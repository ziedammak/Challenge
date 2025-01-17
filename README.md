## Overview

This project automates the process of validating, uploading, and verifying location data from a CSV file using the Cozero API. It provides comprehensive data handling, including:

- Data validation
- API interaction
- Automated uploading
- Detailed reporting

## Prerequisites

### Dependencies

- pandas
- requests
- pytest
- python-dotenv

### Create Virtual Environment

1. First, you need to create a virtual environment for the project to isolate the dependencies. Run the following command in the project root directory:

#### On macOS/Linux:

```bash
python3 -m venv venv
```
On Windows:
```bash
python -m venv venv
```
2. Activate the Virtual Environment
After creating the virtual environment, you need to activate it.

On macOS/Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```


### Installation
```bash
pip install -r requirements.txt
```



## Configuration

### Environment Setup

Create a `.env` file in the project root:

COZERO_EMAIL=your_email@example.com

COZERO_PASSWORD=your_password

## Usage

### Running the Script
```bash
python main.py
```

### Running Tests
```bash
pytest test_validate_data.py
```

## Features

- Comprehensive data validation
- Automatic API authentication
- Batch location upload
- Detailed error reporting
- Location data management

## Validation Checks

- Missing value detection
- Data type validation
- Duplicate name identification

## Output

A detailed `customer_report.log` is generated in the `output/` directory, containing:

- Uploaded data summary
- Validation issues
- API matching report

