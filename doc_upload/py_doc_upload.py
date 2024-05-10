import base64
import os
import uuid
from datetime import datetime as dt
from azure_blob.blob_upload import upload_to_azure_blob, getfile_azure_blob
from db_connection import py_connection


def fn_doc_upload(request, decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        task_fk = request.get("task_fk")
        formData = request.get("formData")
        file = formData['file_upload'].get("data")
        file_size_bytes = len(file)  # File size in bytes
        file_size_kb = int(file_size_bytes / 1024)
        remarks = formData['remarks']
        qry = "SELECT name FROM Web_v_assigned_task WHERE doc_pk = " + str(task_fk)
        res = py_connection.get_result(qry)
        filename, access_key = upload_to_azure_blob(file, decoded, res[0][0])
        sql_command = "{CALL  web_sp_file_upload (?, ?,?, ?, ?, ?)}"
        params = (task_fk, filename, access_key, remarks, comp_fk, file_size_kb)
        py_connection.call_prop(sql_command, params)
        return {"message": "Data Uploaded successfully"}
    except Exception as e:
        print(str(e))
        return {"message": "Something Went Wrong"}


