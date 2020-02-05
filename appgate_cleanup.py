import json
from decouple import config
import requests
import sys

# Functions to retrieve the bear tokens for the dev and stage.
def get_token(passwd, device_id, url_var):
    payload = {"providerName": "local", "username": config('USERNAME_VAR'),
               "password": config(passwd), "deviceId": config(device_id)}
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/vnd.appgate.peer-v11+json'}
    url = config(url_var) + 'login'
    token_post = requests.post(
        url, headers=headers, json=payload, verify=False)
    token_data = token_post.text
    token_string = token_data
    token_clean_string = token_string.replace("'", '"')
    token_dict = json.loads(token_clean_string)
    token = token_dict['token']
    return token

# Function to perform a REST API call to GET data
def get_operations(bear_token, ops_type, url_var):
    headers = {'Authorization': 'Bearer ' + bear_token, 'Content-Type': 'application/json',
               'Accept': 'application/vnd.appgate.peer-v10+json'}
    url = config(url_var) + ops_type
    ops_get = requests.get(url, headers=headers, verify=False)
    if ops_get.status_code == 200:
        print("GET Request Successful!")
    elif ops_get.status_code == 401:
        print("Token error. Login again.")
    elif ops_get.status_code == 403:
        print("Insufficient permissions to access this resource.")
    elif ops_get.status_code == 500:
        print("Unexpected server side error.")
    else:
        print("GET Request Failed")
    ops_data = ops_get.text
    return ops_data

# Function to perform REST API PUT operations
def put_operations(bear_token, operations_data, ops_type, url_var):
    headers = {'Authorization': 'Bearer ' + bear_token,
               'Content-Type': 'application/json',
               'Accept': 'application/vnd.appgate.peer-v11+json'}
    payload = operations_data
    url = config(url_var) + ops_type
    ops_put = requests.put(url, headers=headers, json=payload, verify=False)
    if ops_put.status_code == 200:
        print("PUT Request Successful! Feature Updated!")
    elif ops_put.status_code == 400:
        print("JSON error. Check the JSON format.")
    elif ops_put.status_code == 401:
        print("Token error. Login again.")
    elif ops_put.status_code == 403:
        print("Insufficient permissions to access this resource.")
    elif ops_put.status_code == 404:
        print("The requested resource can not be found.")
    elif ops_put.status_code == 422:
        print('Request validation error. Check "errors" array for details.')
    elif ops_put.status_code == 500:
        print("Unexpected server side error.")
    else:
        print("PUT Request Failed")
    ops_data = ops_put.text
    return ops_data

# Function to perform a REST API call to DELETE data
def del_operations(bear_token, ops_type, url_var):
    headers = {'Authorization': 'Bearer ' + bear_token, 'Content-Type': 'application/json',
               'Accept': 'application/vnd.appgate.peer-v10+json'}
    url = config(url_var) + ops_type
    ops_del = requests.delete(url, headers=headers, verify=False)
    if ops_del.status_code == 204:
        print("DELETE Request Successful!")
    elif ops_del.status_code == 401:
        print("Token error. Login again.")
    elif ops_del.status_code == 403:
        print("Insufficient permissions to access this resource.")
    elif ops_del.status_code == 404:
        print("The requested resource can not be found.")
    elif ops_del.status_code == 500:
        print("Unexpected server side error.")
    else:
        print("DELETE Request Failed")
    ops_data = ops_del.text
    return ops_data

def main():
    env_var = sys.argv[1].lower()
    heimdall_ent_list = []
    heimdall_pol_list = []
    heimdall_tag = "tag_heimdall"
###########################################################################################################################
#             Data Fetching                                                                                               #
###########################################################################################################################

# Loop to read the arguments to know whether dev, stage, or prod will be modified
# To run the program, you need to enter the environment argument in the following form
# python data_import_1_gw.py dev for example

    if env_var == 'dev' or env_var == 'stage':
        ops_url_var = env_var.upper() + '_URL_VAR'
        ops_pwd_var = env_var.upper() + '_PASSWORD_VAR'
        ops_devid_var = env_var.upper() + '_DEVICE_ID_VAR'
    else:
        print("Invalid argument, enter DEV OR STAGE. Exiting...")
        quit()

    """ 
        The next part of the script formats the data taken from the csv file and puts it
        into the REST API entitlement structure, JSON format. 
        Starting with the entitlements and then policies.
        Entitlements are linked to policies using a tag based on the okta application ID
    """
    # Start of REST API call to get the Tokens
    print("Getting Token")
    token = get_token(ops_pwd_var, ops_devid_var, ops_url_var)
    print("*" * 100)
    # Gets the Site ID for AWS and SWE EXT from the relevant environment
    print("Getting Sites Data")
    get_sites = json.loads(get_operations(token, 'sites', ops_url_var))
    print("*" * 100)
    print("Getting Entitlements Data")
    get_entitlements = json.loads(get_operations(token, 'entitlements', ops_url_var))
    print("*" * 100)
    print("Getting Policies Data")
    get_policies = json.loads(get_operations(token, 'policies', ops_url_var))
    print("*" * 100)

    # Loop to fetch AWS ID data
    for site in get_sites['data']:
        site_id = site['id']
        site_name = site['name']
        if site_name == "AWS":
            aws_site_id = site_id
        else:
            pass
    
    # Loop to create an ID List of entitlements to delete
    for entitlement in get_entitlements['data']:
        if heimdall_tag in entitlement['tags']:
            heimdall_ent_list.append(entitlement['id'])
        else:
            pass

    # Loop to create an ID List of policies to delete
    for policy in get_policies['data']:
        if heimdall_tag in policy['tags']:
            heimdall_pol_list.append(policy['id'])
        else:
            pass
    
    aws_site = json.loads(get_operations(token, 'sites/' + aws_site_id, ops_url_var))
    aws_site['nameResolution']['awsResolvers'][0]['assumedRoles'] = []
    

    ###########################################################################################################################
    #             Start of API Calls                                                                                          #
    ###########################################################################################################################
    """ 
        At this stage, the data structure for the entitlements and policies has been created.
        The next step is to perform the REST API calls to GET the bear token, and then 
        POST entitlements and policies.
    """

    # REST API Call to Delete Entitlements
    for entitlement_id in heimdall_ent_list:
        del_operations(token,'entitlements/' + entitlement_id, ops_url_var)
        print( "Entitlement " + entitlement_id )
        print("*" * 100)

    # REST API Call to Delete Policies
    for policy_id in heimdall_pol_list:
        del_operations(token, 'policies/' + policy_id, ops_url_var)
        print("Policy " + entitlement_id )
        print("*" * 100)
    
    # Delete Assumed Roles from AWS Site
    print('\n')
    print("Deleting AWS Assumed Roles to Resolvers")
    put_operations(token, aws_site, 'sites/' + aws_site_id, ops_url_var)

if __name__ == '__main__':
    main()
