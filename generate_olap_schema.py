# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 17:58:54 2019

@author: K.Bjerkelund

source for login: https://github.com/Azure-Samples/data-lake-analytics-python-auth-options
"""

import adal
from msrestazure.azure_active_directory import AADTokenCredentials
import adodbapi
import sys

def authenticate_device_code(tenant,clientId):
    """
    Authenticate the end-user using device auth.
    """
    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = f'{tenant}'
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://api.azuredatacatalog.com/'
    client_id = f'{clientId}'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials


Enumeration	= {
2:	"String",
6:	"Int64",
8:	"Double",
9:	"DateTime",
10:	"Decimal",
11:	"Boolean",
17:	"Binary",
19:	"Unknown",
20:	"Variant"
}


def get_model(token,tenant,modelId):
    conn=adodbapi.connect(f"Provider=MSOLAP;Integrated Security=ClaimsToken;Identity Provider=https://login.microsoftonline.com/common, https://analysis.windows.net/powerbi/api, {tenant};Data Source=pbiazure://api.powerbi.com;Initial Catalog={modelId};Persist Security Info=True;Impersonation Level=Impersonate")
    cur=conn.cursor()
    cur.execute("SELECT * FROM $SYSTEM.TMSCHEMA_TABLES")
    a=cur.fetchall()
    schema={"tables":[]}
    for row in a:
        if row[5]==0:
            schema["tables"].append({"name":row[2],"localid":row[0],"columns":[],"measures":[]})
        
    
    cur.execute("SELECT * FROM $SYSTEM.TMSCHEMA_COLUMNS")
    a=cur.fetchall()
    
    for row in a:
        try:
            idx=next(i for i, x in enumerate(schema["tables"]) if x["localid"] == row[1])
            schema["tables"][idx]["columns"].append({"name":row[2],"type":Enumeration[row[4]]})
        except:
            pass
        
    cur.execute("SELECT * FROM $SYSTEM.TMSCHEMA_MEASURES")
    a=cur.fetchall()
    for row in a:
        try:
            idx=next(i for i, x in enumerate(schema["tables"]) if x["localid"] == row[1])
            schema["tables"][idx]["measures"].append({"name":row[2],"expression":row[5]})
        except:
            pass
    return schema


if __name__ == '__main__':
    tenant = sys.argv[1]
    clientId = sys.argv[2]
    modelId = sys.argv[3]
    creds = authenticate_device_code(tenant,modelId)
    schema = get_model(creds.token,tenant,modelId)
    print(schema)