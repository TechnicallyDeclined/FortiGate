import requests
import json
import time

def create_vlan(fortigate_ip, headers, vlan_data):
    url = f"https://{fortigate_ip}/api/v2/cmdb/system/interface"
    response = requests.post(url, headers=headers, data=json.dumps(vlan_data), verify=False)
    if response.status_code == 200:
        print(f"VLAN {vlan_data['json']['name']} created successfully!")
        return True
    else:
        print(f"Failed to create VLAN {vlan_data['json']['name']}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    # Example usage (you might not run this directly)
    # Replace with your actual IP and headers
    fortigate_ip = "192.168.1.99"
    headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
    vlan_config = {
        "json": {
            "vdom": "root",
            "name": "TEST_VLAN",
            "alias": "Test",
            "vlanid": 999,
            "interface": "fortilink",
            "ip": "10.0.0.1 255.255.255.0",
        }
    }
    create_vlan(fortigate_ip, headers, vlan_config)