from netmiko import ConnectHandler
from getpass import getpass

# Device details
FortiGate = {
    "device_type": "fortinet",
    "host": "192.168.1.99", # Replace with your device IP
    "username": "admin", # Replace with your username
    "password": getpass(), # Password is empty on default FortiGate devices
    }

# Connect to the device
Connection = ConnectHandler(**FortiGate)
print("Connected to the device successfully!")


# Create API user
api_user = input("Enter the API user name: ")
api_commands = [
    "config system api-user",
    f"edit {api_user}",
    "set accprofile super_admin",
    "set vdom root",
    "end",
]

output = Connection.send_config_set(api_commands)
print(output)

# Generate and display the API key
Create_API_key = f"execute api-user generate-key {api_user}"
API_Key_Output = Connection.send_command(Create_API_key)
print(API_Key_Output)

# Disconnect from the device
Connection.disconnect()


