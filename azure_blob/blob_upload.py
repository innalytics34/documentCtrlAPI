import uuid
from db_connection import py_connection
from datetime import datetime as dt, datetime, timedelta
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import base64
import json

connection_string = ("DefaultEndpointsProtocol=https;AccountName=iecstore;AccountKey"
                     "=E52k3gjrBxRZ31swWniFzziNsj5TKrLAxEn/jranR/E+f7BFZpHOnso/tgFXKb5B0VSC09ZJHF85Ma2rsi01pw"
                     "==;EndpointSuffix=core.windows.net")
container_name = "wmpfiles"


def blob_connection(decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        qry = "SELECT connection_string, container_name FROM web_v_organization where comp_pk=" + str(comp_fk)
        result = py_connection.get_result(qry)
        if result:
            blob_service_client = BlobServiceClient.from_connection_string(result[0][0])
            container_client = blob_service_client.get_container_client(result[0][1])
            return container_client
        else:
            raise ValueError("No Azure Blob connection details found in the database.")
    except:
        print("blob connection failed")


def create_accesskey(base64string, length=16):
    splitstring = base64string[:-length]
    access_key = base64string[-length:]
    return splitstring, access_key


def upload_to_azure_blob(base64string, decoded, foldername):
    try:
        container_client = blob_connection(decoded)
        filename = str(uuid.uuid4().hex) + ".json"
        base_dir = os.getenv("FILE_PATH", "../temp_file/")
        blob_client = container_client.get_blob_client(foldername + '/' + filename)
        splitstring, access_key = create_accesskey(base64string)
        data = {'base64string': splitstring}
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        with open(base_dir + filename, 'w') as f:
            json.dump(data, f)
        with open(base_dir + filename, "rb") as data:
            print(data,"___________________")
            blob_client.upload_blob(data)
        os.remove(base_dir + filename)
        return foldername + '/' + filename, access_key
    except Exception as e:
        print("Error uploading file to Azure Blob Storage:", e)


def getfile_azure_blob(blob_name, decoded, doc_fk):
    try:
        container_client = blob_connection(decoded)
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        data = json.loads(blob_data)
        properties = blob_client.get_blob_properties()
        read_size = int(properties.size / 1024)
        updatefilereadlog(read_size, decoded, doc_fk)
        return data['base64string']
    except Exception as e:
        print("Error downloading file from Azure Blob Storage:", e)


def updatefilereadlog(read_size, decoded, doc_fk):
    comp_fk = decoded.get('comp_fk')
    emp_fk = decoded.get('emp_fk')
    qry = "insert into Web_file_readlog(read_size, comp_fk, emp_fk, doc_fk, dt) values(?,?,?,?,?)"
    values = (read_size, comp_fk, emp_fk, doc_fk, dt.now())
    py_connection.put_result(qry, values)


