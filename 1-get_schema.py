import adodbapi

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

def get_model_schema(token,tenant,modelId):
    conn=adodbapi.connect(f"Provider=MSOLAP;Integrated Security=ClaimsToken;Identity Provider=https://login.microsoftonline.com/common, https://analysis.windows.net/powerbi/api, {tenant};Data Source=pbiazure://api.powerbi.com;Initial Catalog={modelId};Persist Security Info=True;Impersonation Level=Impersonate;Password={token}")
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