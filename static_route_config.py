from fortigate_api_client import send_api_request, handle_api_response
import time

# This will configure the Static route on the wan interface
def create_static_route(fortigate_ip, headers, static_route_data):
    endpoint = f"router/static"
    response = send_api_request(fortigate_ip, endpoint, headers, method="POST", data=static_route_data)
    return handle_api_response(response, "Static route", "configured successfully", "check the fortigate api response")

def update_static_route(fortigate_ip, headers, static_route_data):
    endpoint = f"router/static/{static_route_data['id']}"
    response = send_api_request(fortigate_ip, endpoint, headers, method="PUT", data=static_route_data)
    return handle_api_response(response, "Static route", "updated successfully", "check the fortigate api response")

def get_static_routes(fortigate_ip, headers):
    endpoint = "router/static"
    response = send_api_request(fortigate_ip, endpoint, headers, method="GET")
    return handle_api_response(response, "Static route", "retrieved successfully", "check the fortigate api response")

def delete_static_route(fortigate_ip, headers, route_id):
    endpoint = f"router/static/{route_id}"
    response = send_api_request(fortigate_ip, endpoint, headers, method="DELETE")
    return handle_api_response(response, "Static route", "deleted successfully", "check the fortigate api response")

if __name__ == "__main__":
    # Example usage (for testing the module directly)
    # Replace with your actual IP and headers
    fortigate_ip = "your_fortigate_ip"
    headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

    example_route_create = {
        "dst": "192.168.2.0/24",
        "gateway": "10.0.1.1",
        "device": "port1",
        "distance": 10,
        "status": "enable"
    }

    print("Attempting to create a static route:")
    if create_static_route(fortigate_ip, headers, example_route_create):
        print("Static route creation initiated.")
        time.sleep(5)  # Give it some time to be created

        # Example of getting static routes
        routes = get_static_routes(fortigate_ip, headers)
        if routes:
            print("\nExisting static routes:")
            for route in routes:
                print(route)
            # Let's try to update the one we just created (you'd typically identify it better)
            if routes:
                first_route_id = routes[0].get('id')
                if first_route_id:
                    example_route_update = {
                        "distance": 20,
                        "status": "disable"
                    }
                    print(f"\nAttempting to update static route with ID '{first_route_id}':")
                    update_static_route(fortigate_ip, headers, first_route_id, example_route_update)
                    time.sleep(5)

                    print(f"\nAttempting to delete static route with ID '{first_route_id}':")
                    delete_static_route(fortigate_ip, headers, first_route_id)
                else:
                    print("Could not find the ID of the newly created route for update/delete example.")
        else:
            print("Could not retrieve static routes to proceed with update/delete example.")
    else:
        print("Failed to initiate static route creation.")