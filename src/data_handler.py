import pandas as pd

def check_required_columns(df, required_columns):
    """Check if required columns are missing values."""
    missing_values = {}

    for col in required_columns:
        missing = df[col].isnull() | (df[col] == '')
        if missing.any():
            missing_values[col] = df[missing]

    return missing_values

def check_column_types(df, column_rules):
    """Check the data types of each column according to the rules."""
    invalid_data = {}

    for col, (expected_type, is_optional) in column_rules.items():
        if not is_optional:
            invalid = ~df[col].apply(lambda x: isinstance(x, expected_type) or pd.isnull(x))
            if invalid.any():
                invalid_data[col] = df[invalid]

    return invalid_data

def check_unique_names(df):
    """Check for duplicate 'Name' values in the DataFrame."""
    duplicate_names = df[df.duplicated(subset='Name', keep=False)]
    return duplicate_names

def validate_data(df):
    """Validate data according to the schema rules."""
    required_columns = ['Name', 'Business Unit ID', 'Address']

    # Check missing required columns
    missing = check_required_columns(df, required_columns)

    # Check data types based on the schema
    column_rules = {
        'Name': (str, False),
        'Description': (str, True),
        'Business Unit ID': (int, False),
        'User ID': (int, True),
        'Address': (str, False),
        'Tag': (str, True),
    }
    invalid_types = check_column_types(df, column_rules)

    # Check for duplicate names
    duplicate_names = check_unique_names(df)

    return missing, invalid_types, duplicate_names
