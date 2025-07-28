from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) [X] Creating a function to test the PATCH request /store/order/{order_id}
2) [X] *Optional* Consider using @pytest.fixture to create unique test data for each run
2) [ ] *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) [X] Validate the response codes and values
4) [X] Validate the response message "Order and pet status updated successfully"
'''
@pytest.fixture
def create_test_order():
    """
    Fixture to create a test order. This order will be used and updated in the test.
    """
    # Data for creating a test order
    order_data = {
        "pet_id": 0,
    }

    # Send the POST request to create a new order
    response = api_helpers.post_api_data("/store/order", order_data)

    # Validate the response status code
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Return the created order data for use in tests
    return response.json()

def test_patch_order_by_id(create_test_order):
    """
    Test to validate the PATCH request to update an order by ID.
    """
    # Use the order ID from the fixture
    order_id = create_test_order["id"]

    # Data to update the order
    patch_data = {
        "status": "sold"  # Update the status of the order
    }

    # Send the PATCH request
    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_data)

    # Validate the response status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate the response message
    response_body = response.json()
    assert_that(response_body.get("message"), contains_string("Order and pet status updated successfully"))
