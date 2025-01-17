import os 

def generate_customer_report(uploaded_data, api_data, missing, invalid_types, duplicate_names, output_file="output/customer_report.log"):
    """
    Generates a log file for reporting the uploaded data, validation issues, and discrepancies.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    
    # Check if the directory exists, if not, create it
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("=== Customer Data Report ===\n\n")

        # Uploaded Data Report
        file.write("Uploaded Data:\n")
        if uploaded_data:
            for idx, uploaded_item in enumerate(uploaded_data, start=1):
                file.write(f" - Record {idx}: {uploaded_item}\n")
            file.write("\n")
        else:
            file.write("No uploaded data provided.\n\n")

        # Validation Issues
        file.write("Validation Issues:\n\n")

        # Missing Required Values
        if missing:
            file.write("Missing Required Values:\n")
            for col, rows in missing.items():
                for index in rows.index:
                    file.write(f" - Row {index}: Missing value in column '{col}'\n")
            file.write("\n")
        else:
            file.write("No missing required values found.\n\n")

        # Invalid Data Types
        if invalid_types:
            file.write("Invalid Data Types:\n")
            for col, rows in invalid_types.items():
                for index in rows.index:
                    file.write(f" - Row {index}: Invalid value in column '{col}'\n")
            file.write("\n")
        else:
            file.write("No invalid data types found.\n\n")

        # Duplicate Names
        if duplicate_names is not None and not duplicate_names.empty:
            file.write("Duplicate Names Found:\n")
            for index, row in duplicate_names.iterrows():
                file.write(f" - Row {index}: {row.to_dict()}\n")
            file.write("\n")
        else:
            file.write("No duplicate names found.\n\n")

        # API Matching Report
        file.write("API Matching Report:\n")
        if uploaded_data and api_data:
            for uploaded_item in uploaded_data:
                # Find matching API entry by name
                api_match = next((item for item in api_data if item["name"].strip() == uploaded_item["Name"].strip()), None)
                
                if api_match:
                    file.write(f" - {uploaded_item['Name']} found in API data (ID: {api_match['id']}, Address: {api_match['address']})\n")
                else:
                    file.write(f" - {uploaded_item['Name']} not found in API data.\n")
            file.write("\n")
        else:
            file.write("No data to compare with API.\n\n")

        file.write("=== End of Report ===\n")

    print(f"Customer report saved to '{output_file}'.")


