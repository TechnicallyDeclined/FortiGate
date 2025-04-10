from fortigate_api_client import send_api_request, handle_api_response

# This will configure the Static route on the wan interface
def create_static_route(fortigate_ip, headers, static_route_data):
    endpoint = f"router/static"
    response = send_api_request(fortigate_ip, endpoint, headers, method="POST", data=static_route_data)
    return handle_api_response(response, "Static route", "configured successfully", "check the fortigate api response")

def update_static_route(fortigate_ip, headers, static_route_data):
    endpoint = f"router/static/{static_route_data['id']}"
    response = send_api_request(fortigate_ip, endpoint, headers, method="PUT", data=static_route_data)
    return handle_api_response(response, "Static route", "updated successfully", "check the fortigate api response")

def get_static_route(fortigate_ip, headers):
    endpoint = "router/static"
    response = send_api_request(fortigate_ip, endpoint, headers, method="GET")
    return handle_api_response(response, "Static route", "retrieved successfully", "check the fortigate api response")

def delete_static_route(fortigate_ip, headers, route_id):
    endpoint = f"router/static/{route_id}"
    response = send_api_request(fortigate_ip, endpoint, headers, method="DELETE")
    return handle_api_response(response, "Static route", "deleted successfully", "check the fortigate api response")