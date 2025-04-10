import getpass
import time
from fortinet_api_module import get_fortigate_api_key
from config_manager import load_config  # Import the load_config function
from forti_vlans_module import create_vlan  # Assuming you only kept create_vlan in vlan_config.py
from wan_config import configure_wan_interface
from static_route_config import create_static_route
from zone_config import create_zone
from policy_config import create_firewall_policy
from user_config import create_user

if __name__ == "__main__":
    config = load_config(config_file="config.yaml")  # Load configuration from config.yaml
    if not config:
        exit()

    fortigate_ip = config.get('fortigate_ip')
    username = config.get('username')

    passwd_api_key = getpass.getpass(f'Please enter the FortiGate password for API key retrieval on {fortigate_ip}: ')
    api_username_to_create = input("Enter the API username to create: ")

    api_key = get_fortigate_api_key(fortigate_ip, username, passwd_api_key, api_username_to_create)

    if api_key:
        print(f"Successfully retrieved API Key: {api_key}")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Configure VLANs
        for vlan_config in config.get('vlans', []):
            if create_vlan(fortigate_ip, headers, vlan_config):
                time.sleep(2)

        # Configure WAN1
        wan1_config = config.get('wan1')
        if wan1_config:
            configure_wan_interface(fortigate_ip, headers, wan1_config)
            time.sleep(2)

        # Configure static route
        static_route_config = config.get('static_route')
        if static_route_config:
            create_static_route(fortigate_ip, headers, static_route_config)
            time.sleep(2)

        # Configure zone
        zone_name = config.get('zone_name')
        vlans_config = config.get('vlans', [])
        if zone_name and vlans_config:
            vlan_names = [v['name'] for v in vlans_config]
            create_zone(fortigate_ip, headers, zone_name, vlan_names)
            time.sleep(2)

        # Configure firewall policy
        policy_name = config.get('policy_name')
        if policy_name and zone_name:
            policy_data = {
                "name": policy_name,
                "srcintf": [{"name": zone_name}],
                "dstintf": [{"name": "wan1"}],
                "action": "accept",
                "status": "enable",
                "srcaddr": [{"name": "all"}],
                "dstaddr": [{"name": "all"}],
                "service": [{"name": "ALL"}],
                "schedule": "always",
                "nat": "enable"
            }
            create_firewall_policy(fortigate_ip, headers, policy_data)
            time.sleep(2)

        # Create tech user
        tech_user_config = config.get('tech_user')
        if tech_user_config:
            tech_password = getpass.getpass(f"Please enter the password for the 'tech' user on {fortigate_ip}: ")
            tech_data = {
                "json": {
                    "vdom": "root",
                    "name": tech_user_config.get('name', 'tech'),
                    "password": tech_password,
                    "status": "enable",
                    "accprofile": "super_admin",
                    "trustedhosts": tech_user_config.get('trustedhosts', [])
                }
            }
            create_user(fortigate_ip, headers, tech_data)
            time.sleep(2)

        print("FortiGate configuration process completed.")

    else:
        print("Failed to load configuration. Exiting.")