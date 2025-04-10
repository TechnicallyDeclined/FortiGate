import requests
import json

# Create function to send the API requests. 
def send_api_request(fortigate_ip, headers, method, endpoint, data=None, verify=False):
    url = "f:https://{fortigate_ip}/api/v2/{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data), verify=verify)
        elif method == "PUT":
            resonse = requests.put(url, headers=headers, data=json.dumps(data), verify=verify)
        elif method == "GET":
            response = requests.get(url, headers=headers, verify=verify)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, verify=verify)
        else:
            print(f"Error: Unsupported method '{method}',")
            return None
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Apie request failed for {endpoint}: {e}")
        if response is not None:
            print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response from {endpoint}")
        if response is not None:
            print(f"Response: {response.text}")
        return None
    
    # Takes the response from the AIP and prints the messages
def handle_api_response(response, resource_name, success_message, failure_message):
        if response and response['status'] == 'success':
            print(f"{resource_name} {success_message}")
            return True
        else: 
            print(f"Failed to configure {resource_name}, {failure_message}")
            if response and 'results' in response and response['results']:
                print(f"Error message: {response['results'][0].get['message']}")
            return False
    
