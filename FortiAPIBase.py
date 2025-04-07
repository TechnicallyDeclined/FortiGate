import requests
import json
import getpass
from fortinet_api_module import get_fortigate_api_key
#####################################################
##
##
## Hunter's Automated FortiAPI Configuration Script
##
##
####################################################


####################################################
## This script is designed to automate the configuration of a FortiGate firewall using the FortiAPI.
## It includes the following features: Vlan configuration, DHCP relay setup, WAN interface configuration, static route setup, zone creation, firewall policy creation, and user account creation.
## Will be adding more features in the future such as SD-WAN, VPN, and other configurations.
## Will implement a automated way to create the API token in the future as well.
## Netmiko will be used most likely for the CLI commands in the future. Such as creating the API token, and deleting the default admin account. Need to look into its capabilities for the FortiGate CLI.
## Recommend to verify the configuration after running the script to ensure everything is set up correctly.
####################################################



# Variable for the tech password
passwd = getpass.getpass('Please enter the password: ')
api_username_to_create = input("Enter the API username to create: ")

# Define the FortiGate API IP and credentials
fortigate_ip = "192.168.1.99"  # Replace with your FortiGate's IP address
username = "admin"  # Replace with your FortiGate username

api_key = get_fortigate_api_key(fortigate_ip, username, passwd, api_username_to_create)

if api_key:
    print(f"Successfully retrieved API Key: {api_key}")
    # Now you can use the 'api_key' variable for your API calls
else:
    print("Failed to retrieve the API key.")

# Dictionary that defines the VLAN configurations (multiple VLANs)
vlans = [
    {
        "name": "VLAN10",
        "alias": "Data",
        "vlanid": 10,
        "interface": "fortilink",
        "ip": "10.35.13.1 255.255.255.0", # Example 192.168.1.1 255.255.255.0
       # Comment out the lines below if you are using DHCP relay
        "dhcp_range": ("10.35.13.100", "10.35.13.200"),
        "default_gateway": "10.35.13.1",
        "dns_servers": ["8.8.8.8", "8.8.4.4"]
    },
    {
        "name": "VLAN99",
        "alias": "Management",
        "vlanid": 99,
        "interface": "fortilink",
        "ip": "gateway of vlan", # Example 192.168.1.1 255.255.255.0
       # Comment out the lines below if you are using DHCP relay
        "dhcp_range": ("Start of pool", "End of Pool"),
        "default_gateway": "192.168.100.1",
        "dns_servers": ["8.8.8.8", "8.8.4.4"]
    },
]

# Set the headers for the request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Loop through each VLAN configuration and send a POST request ## Comment out the dhcp-relay-service and dhcp-relay-ip in the vlans dictionary to remove them from the configuration.
for vlan in vlans:
    vlan_data = {
        "json": {
            "vdom": "root",
            "name": vlan["name"],
            "alias": vlan["alias"],
            "vlanid": vlan["vlanid"],
            "interface": vlan["interface"],
            "ip": vlan["ip"],
        # Uncomment the following lines if you want to enable DHCP relay for each VLAN
           # "dhcp-relay-service": "enable",  # Enable DHCP relay service
           # "dhcp-relay-ip": "<dhcp server ip address>",  # DHCP server IP
           # "dhcp-relay-type": "regular",  # Type of relay
           # "dhcp-relay-agent-option": "enable",  # Enable DHCP relay agent option
           # "dhcp-relay-interface": "",
           # "dhcp-relay-interface-select-method": "auto"  # Method for selecting the relay interface   
            
        }
    }

    # Send the POST request to create the VLAN
    url = f"https://{fortigate_ip}/api/v2/cmdb/system/interface"
    response = requests.post(url, headers=headers, data=json.dumps(vlan_data), verify=False)

    # Check the response
    if response.status_code == 200:
        print(f"VLAN {vlan['name']} created successfully!")
    else:
        print(f"Failed to create VLAN {vlan['name']}. Status code: {response.status_code}")
        print(f"Response: {response.text}")


# DHCP Server configuration for VLANs, VLANs need to be created first before configuring DHCP server.
# Uncomment the following lines if you want to configure DHCP relay for each VLAN
dhcp_info = {
    "interface": f"vlan{vlan['vlanid']}",
    "lease_time": 86400,  # Lease time in seconds (1 day)
    "netmask": "255.255.255.0:",
    "range": [
       {
        "start": vlan["dhcp_range"][0],
        "end": vlan["dhcp_range"][1] 
        }   
    ],
    "status": "enable",
    "default-gateway": vlan["default_gateway"],
    "dns-server": vlan["dns_servers"],
}

dhcp_url = f"https://{fortigate_ip}/api/v2/cmdb/system.dhcp/server"
dhcp_response = requests.post(dhcp_url, headers=headers, data=json.dumps(dhcp_info), verify=False)

if dhcp_response.status_code == 200:
    print(f"DHCP server for VLAN{vlan['vlanid']} configured successfully!") 
else:
    print(f"Failed to configure DHCP server for VLAN{vlan['vlanid']}. Status code: {dhcp_response.status_code}")
    print(f"Response: {dhcp_response.text}")


#############################################
# 
# Would like to add the configuration of SD-WAN here as well. 
#
#############################################
# Configure WAN1 interface as static or dhcp
wan1_data = {
    "json": {
        "vdom": "root",
        "name": "wan1",
        "mode": "static",  # Static/dhcp
        "ip": "66.171.17.248 255.255.255.0",  # uncomment and configure ip address 0.0.0.0 0.0.0.0
        "allowaccess": "ping https ssh http"  # Allow certain management access
    }
}

# Send the PUT request to configure the WAN1 interface
url = f"https://{fortigate_ip}/api/v2/cmdb/system/interface/wan1"
response = requests.put(url, headers=headers, data=json.dumps(wan1_data), verify=False)

# Check the response for configuring WAN1 interface
if response.status_code == 200:
    print("WAN1 interface configured successfully!")
else:
    print(f"Failed to configure WAN1. Status code: {response.status_code}")
    print(f"Response: {response.text}")

##################################################################################################


# Configuration for static route if no DHCP uncomment if needed.
static_route_data = {
    "json": {
        "vdom": "root",
        "dst": "0.0.0.0/0",  # Default route (all traffic)
        "gateway": "66.171.17.1",  # Gateway IP address for WAN1
        "device": "wan1",  # Use WAN1 interface
        "distance": 10,  # Routing distance, lower is higher priority
        "status": "enable"  # Enable the static route
    }
}

# Send the POST request to configure the static route
url = f"https://{fortigate_ip}/api/v2/cmdb/router/static"
response = requests.post(url, headers=headers, data=json.dumps(static_route_data), verify=False)

# Check the response for adding the static route
if response.status_code == 200:
   print("Static route configured successfully!")
else:
    print(f"Failed to configure static route. Status code: {response.status_code}")
    print(f"Response: {response.text}")

####################################################################################################

# Create the zones and add the VLAN interfaces to zones
zone_name = "Vlans"  # This is the name of the zone we are creating

# Extract the VLAN interface names from the 'vlans' dictionary
vlan_interfaces = []
for vlan in vlans:
    vlan_name = {"interface-name": vlan["name"]}  # Format as {"interface-name": "VLAN10"}
    vlan_interfaces.append(vlan_name) 

#####
# Need to fine tune the Zone creation. Currently inter-vlan routing is configured as default. 
#####

# Create the zone with the VLAN interfaces 
zone_data = {
    "json": {
        "vdom": "root",
        "name": zone_name,
        "interface": vlan_interfaces # this will add all of the vlan interfaces from the vlans dictionary
    }
} 

# Send the POST request to create the zone
url = f"https://{fortigate_ip}/api/v2/cmdb/system/zone"
response = requests.post(url, headers=headers, data=json.dumps(zone_data), verify=False)

# Check the response for creating the zone
if response.status_code == 200:
    print(f"Zone '{zone_name}' created successfully and VLANS added!")
else: 
    print(f"Failed to create zone. Status code: {response.status_code}")
    print(f"Response: {response.text}")

    # Create a firewall policy to allow traffic between VLANs and other zones/interfaces
policy_data = {
    "json": {
        "vdom": "root",
        "name": "Outside_access",  # Name of the firewall policy
        "srcintf": [{"name": zone_name}],  # Source interface (zone)
        "dstintf": [{"name": "wan1"}],  # Destination interface (for example, WAN interface)
        "action": "accept",  # Action to accept the traffic
        "status": "enable",  # Enable the policy
        "srcaddr": [{"name": "all"}],  # Source addresses (any source)
        "dstaddr": [{"name": "all"}],  # Destination addresses (any destination)
        "service": [{"name": "ALL"}],  # Allow all services (you can specify protocols like HTTP, HTTPS, etc.)
        "schedule": "always",  # Always apply the policy
        "nat": "enable" # Enable/Disable NAT (Network Address Translation) for the policy
    }
}

# Send the POST request to create the firewall policy
url = f"https://{fortigate_ip}/api/v2/cmdb/firewall/policy"
response = requests.post(url, headers=headers, data=json.dumps(policy_data), verify=False)

# Check the response for creating the firewall policy
if response.status_code == 200:
    print(f"Firewall policy 'Allow_VLANs_Traffic' created successfully!")
else:
    print(f"Failed to create firewall policy. Status code: {response.status_code}")
    print(f"Response: {response.text}")

   ##################################################################
   #
   # Setup Remote access VPN/SSL VPN/IPSEC VPN here. Will be added in the next version.
   #
   ##################################################################
   
   
    # Data for the "tech" account
tech_data = {
    "json": {
        "vdom": "root",  
        "name": "tech",  
        "password": passwd,  
        "status": "enable",
        "accprofile": "super_admin",
        "trustedhosts": ["0.0.0.0/32", "0.0.0.0/32", "0.0.0.0/32"] 
    }
}


# Send the POST request to create the "tech" account
url = f"https://{fortigate_ip}/api/v2/cmdb/system/admin"
response = requests.post(url, headers=headers, data=json.dumps(tech_data), verify=False)

# Check the response for creating the "tech" account
if response.status_code == 200:
    print("tech user created successfully with trusted hosts!")
else:
    print(f"Failed to create tech. Status code: {response.status_code}")
    print(f"Response: {response.text}")