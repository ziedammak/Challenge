import pytest
import pandas as pd
from src.data_handler import validate_data

def test_validate_data():
    # Prepare a test DataFrame with missing 'Name' value (set None or empty string)
    data = pd.DataFrame({
        'Name': ['Location A', None, 'Location C'],  # Second entry is missing (None)
        'Description': ['Description A', 'Description B', ''],
        'Business Unit ID': [1, 2, 3],
        'User ID': [1, 2, 3],  # Valid User IDs
        'Address': ['Address A', 'Address B', 'Address C'],
        'Tag': ['Tag1', 'Tag2', 'Tag3'],
    })

    # Call validate_data to get the missing, invalid_types, and duplicate names
    missing, invalid_types, duplicate_names = validate_data(data)

    # Test for missing values
    assert len(missing) == 1  # The 'Name' column has a missing value (None)
    assert 'Name' in missing  # Check that 'Name' is indeed the column with missing data

    # Test for invalid types (User ID column should not contain invalid types)
    assert 'User ID' not in invalid_types  # User ID should not be in invalid_types

    # Test for duplicate names
    assert duplicate_names.empty  # No duplicates in the 'Name' column

# Run the tests
if __name__ == "__main__":
    pytest.main()
