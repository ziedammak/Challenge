import os
import logging
import pandas as pd
from dotenv import load_dotenv
from src.api_handler import CozeroAPI
from src.data_handler import validate_data
from src.utils import generate_customer_report

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_data(file_path):
    """Load the CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Data from {file_path} loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        raise

def process_data(data, api):
    """Process the data: validate, upload and verify."""
    # Validate the data
    missing, invalid_types, duplicate_names = validate_data(data)

    # Filter out invalid data
    valid_locations = data.copy()
    for col, missing_rows in missing.items():
        valid_locations = valid_locations[~valid_locations[col].isin(missing_rows[col])]

    for col, invalid_rows in invalid_types.items():
        valid_locations = valid_locations[~valid_locations[col].isin(invalid_rows[col])]

    valid_locations = valid_locations.drop_duplicates(subset="Name")
    valid_locations = valid_locations.fillna("")
    
    # Upload valid data
    for _, row in valid_locations.iterrows():
        location_data = {
            "name": row["Name"],
            "address": row["Address"],
            "businessUnitId": row["Business Unit ID"],
            "description": row.get("Description", ""),
            "metadata": {"tags": [row.get("Tag", "")]},
            "responsible": {"id": row["User ID"]},
        }
        logging.info(f"Uploading data for location: {row['Name']}")
        api.upload_location(location_data)

    # Fetch uploaded data
    uploaded_data = api.fetch_locations()

    # Generate a customer report
    generate_customer_report(
        uploaded_data=valid_locations.to_dict(orient="records"),
        api_data=uploaded_data,
        missing=missing,
        invalid_types=invalid_types,
        duplicate_names=duplicate_names
    )


def main():
    email = os.getenv("COZERO_EMAIL")
    password = os.getenv("COZERO_PASSWORD")
    api = CozeroAPI(email, password)

    try:
        # Authenticate with API
        api.authenticate()
        logging.info("Authentication successful.")

        # Get user and business unit IDs
        user_id = api.get_user_id()
        business_unit_id = api.get_business_units()

        # delete locations
        delete_confirmation = "yes"
        if delete_confirmation == "yes":
            api.delete_all_locations()
            print("All locations deleted successfully.")
        else:
            print("Deletion skipped.")

        # Load and process data
        data = load_data("data/locations.csv")
        data["User ID"] = user_id
        data["Business Unit ID"] = business_unit_id

        process_data(data, api)

    except Exception as e:
        logging.error(f"Error in processing: {e}")
        raise

if __name__ == "__main__":
    main()
