from fortigate_api_client import send_api_request, handle_api_response
import time

def configure_wan_interface(fortigate_ip, headers, wan1_config):
    """Configures a WAN interface on the FortiGate."""
    wan_name = wan1_config.get('name', 'wan1')  # Default to 'wan1' if name is not provided
    endpoint = f"system/interface/{wan_name}"
    response = send_api_request(fortigate_ip, headers, 'PUT', endpoint, data={"json": wan1_config})
    return handle_api_response(response, f"Interface '{wan_name}'", "configured successfully!", "Check the FortiGate API response.")

if __name__ == "__main__":
    # Example usage (for testing the module directly)
    # Replace with your actual IP and headers
    fortigate_ip = "your_fortigate_ip"
    headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
    example_wan_config = {
        "name": "wan1",
        "mode": "static",
        "ip": "203.0.113.10 255.255.255.0",
        "allowaccess": "ping https ssh http",
        "gateway": "203.0.113.1"
    }
    if configure_wan_interface(fortigate_ip, headers, example_wan_config):
        print("Example WAN1 configuration attempted.")
    else:
        print("Example WAN1 configuration failed.")

    example_dhcp_wan_config = {
        "name": "wan2",
        "mode": "dhcp",
        "allowaccess": "ping http"
    }
    if configure_wan_interface(fortigate_ip, headers, example_dhcp_wan_config):
        print("Example WAN2 (DHCP) configuration attempted.")
    else:
        print("Example WAN2 (DHCP) configuration failed.")