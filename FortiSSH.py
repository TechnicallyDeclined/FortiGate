from netmiko import ConnectHandler
from getpass import getpass

# Device details
FortiGate = {
    "device_type": "fortinet",
    "host": "192.168.1.99", # Replace with your device IP
    "username": "admin", # Replace with your username
    "password": "", # Password is empty on default FortiGate devices
    }

# Connect to the device
Connection = ConnectHandler(**FortiGate)
if Connection:
    print("Connected to the device successfully!")
else:
    print("Failed to connect to the device.") # Print connection status

# The FortiGate will prompt for a password, so we need to provide it
password = getpass(prompt='Enter the password: ')
confirm_password = getpass(prompt='Confirm the password: ')
if password != confirm_password:
    print("Passwords do not match. Exiting...")
    exit(1)

# Prompt for the password and confirm it
Connection.send_command(password)
Connection.send_command(confirm_password)
print("Password set successfully!")

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


