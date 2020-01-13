import adal
from msrestazure.azure_active_directory import AADTokenCredentials

def authenticate_device_code(tenant):
    """
    Authenticate the end-user using device auth.
    """
    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = f"{tenant}"
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://api.azuredatacatalog.com/'
    # This clientId is used for many azure samples, so it's safe for testing :)
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials