from netmiko import ConnectHandler
from getpass import getpass


def get_fortigate_api_key(host, username, password, api_username):
    """
    Connects to a FortiGate device, creates an API user, and retrieves the API key.

    Args:
        host (str): The IP address or hostname of the FortiGate.
        username (str): The username to connect with.
        password (str): The password for the user.
        api_username (str): The desired name for the API user.

    Returns:
        str: The API key if successful, None otherwise.
    """
    Connection = None
    api_key_value = None
    try:
        device = {
            "device_type": "fortinet",
            "host": host,
            "username": username,
            "password": password,
        }
        Connection = ConnectHandler(**device)
        print(f"Connected to {host} successfully!")

        # Create API user
        api_commands = [
            "config system api-user",
            f"edit {api_username}",
            "set accprofile super_admin",
            "set vdom root",
            "end",
        ]
        output = Connection.send_config_set(api_commands)
        print(output)

        # Generate and display the API key
        create_api_key_command = f"execute api-user generate-key {api_username}"
        api_key_output = Connection.send_command(create_api_key_command)
        print(api_key_output)

        # Extract the API key
        for line in api_key_output.splitlines():
            if "API Key:" in line:
                api_key_value = line.split("API Key:")[1].strip()
                break

        return api_key_value

    except Exception as e:
        print(f"An error occurred in get_fortigate_api_key: {type(e)}, {e}")
        return None
    finally:
        if Connection and Connection.is_alive():
            Connection.disconnect()

if __name__ == "__main__":
    fortigate_ip = input("Enter the FortiGate IP address: ")
    username = input("Enter the FortiGate username: ")
    password = getpass("Enter the FortiGate password: ")
    api_user_to_create = input("Enter the API username to create: ")

    api_key = get_fortigate_api_key(fortigate_ip, username, password, api_user_to_create)

    if api_key:
        print(f"\nGenerated API Key for user '{api_user_to_create}': {api_key}")
    else:
        print("Failed to generate the API key.")