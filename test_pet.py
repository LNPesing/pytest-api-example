from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "pending", "sold"])  # Added parameterization for all available statuses
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status  # Added 'status' parameter to filter pets by their status
    }

    response = api_helpers.get_api_data(test_endpoint, params)

    # Validate the response status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"  # Ensures the API returns the correct status code

    # Validate the schema for each object in the response
    pets = response.json()
    for pet in pets:
        validate(instance=pet, schema=schemas.pet)  # Validates each pet object against the defined schema

        # Validate the 'status' property in each object
        assert pet.get("status") == status, f"Expected status '{status}', got '{pet.get('status')}'"  # Ensures the 'status' field matches the requested status
'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("pet_id", [99999])  # Parameterized with edge case pet IDs
def test_get_by_id_404(pet_id):
    """
    Test to validate that the API returns a 404 response for invalid pet IDs.
    Edge cases include:
    - Non-existent large ID (99999)
    """
    test_endpoint = f"/pets/{pet_id}"  # Construct the endpoint with the pet ID

    response = api_helpers.get_api_data(test_endpoint)  # Make the API call

    # Validate the response status code
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"  # Ensure the API returns 404 for invalid IDs

    # Optionally, validate the response body contains an appropriate error message
    error_message = response.json().get("message", "")
    assert_that(error_message, contains_string("not found"))  # Check if the error message contains "not found"
