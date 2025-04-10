from fortigate_api_client import send_api_request, handle_api_response
import time

def create_zone(fortigate_ip, headers, zone_data):
    """
    Create a zone in FortiGate with the specified configuration
    """
    endpoint = f"system/zone"
    # Extract zone name and interfaces from zone_data
    zone_name = zone_data['name']
    vlans_config = zone_data['vlans']
    
    zone_data = {
        "name": zone_name,
        "interface": vlans_config,
        "intrazone": "allow"
    }
    # Send POST request to create the zone
    response = send_api_request(fortigate_ip, headers, endpoint, "POST", zone_data)
    return handle_api_response(response, f"Zone {zone_name}")