import requests

class CozeroAPI:
    BASE_URL = "https://api.cozero.io/v1"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.user_id = None
        self.business_unit_id = None
        self.organization_id = "12119"  # Provided in the task

    def authenticate(self):
        url = f"{self.BASE_URL}/auth/basic"
        payload = {"email": self.email, "password": self.password}
        headers = {"accept": "application/json", "content-type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json()["accessToken"]

    def get_user_id(self):
        url = f"{self.BASE_URL}/central/users/me"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.user_id = response.json()["id"]
        return self.user_id

    def get_business_units(self):
        url = f"{self.BASE_URL}/central/business-units/user-business-units-forest"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params={"organizationId": self.organization_id})
        response.raise_for_status()
        self.business_unit_id = response.json()[0]["value"]
        return self.business_unit_id

    def upload_location(self, location_data):
        url = f"{self.BASE_URL}/central/locations"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, json=location_data, headers=headers)
        response.raise_for_status()
        return response.json()

    def fetch_locations(self):
        if not self.business_unit_id:
            raise ValueError("Business Unit ID is not set. Please authenticate and fetch business units first.")

        url = f"{self.BASE_URL}/central/locations/search"
        headers = {"Authorization": f"Bearer {self.token}", "content-type": "application/json"}
        params = {"selectedBusinessUnitId": self.business_unit_id, "organizationId": self.organization_id}
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def delete_location(self, location_id):
        """Delete a specific location by ID."""
        if not self.user_id:
            raise ValueError("User ID is not set. Please authenticate and fetch user details first.")
        
        url = f"{self.BASE_URL}/central/locations/{location_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json"
        }
        params = {
            "userId": self.user_id,
            "organizationId": self.organization_id
        }

        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        print(f"Deleted location with ID: {location_id}")

    def delete_all_locations(self):
        """Fetch all locations and delete them one by one."""
        locations = self.fetch_locations()
        for location in locations:
            location_id = location["id"]
            self.delete_location(location_id)
        print("All locations have been deleted.")

