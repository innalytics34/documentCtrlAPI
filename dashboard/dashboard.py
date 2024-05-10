
import ast

from azure_blob.blob_upload import getfile_azure_blob
from db_connection import py_connection
import pytz
from datetime import datetime
from filter.py_filter import get_repeatlst, get_emp_details


def get_inputfield(request):
    try:
        task_type = request.get("task_type")
        qry1 = "select input_fields,input_type,id_name from Web_inputfields where task_type=" + str(task_type) + " and status = 1"
        qry2 = "select name from Web_tasklist where tasklist_pk=" + str(task_type)
        result, k = py_connection.get_result_col(qry1)
        taskname = py_connection.get_result(qry2)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                if row[1] == 'dropdown':
                    if row[2] == 'repeat':
                        view_data['dp'] = get_repeatlst()['repeat_lst']
                    elif row[2] =='checker':
                        view_data['dp'] = get_emp_details()['emp_lst']
                    elif row[2] =='assignee':
                        view_data['dp'] = get_emp_details()['emp_lst']
                lst.append(view_data)
            return {"fields": lst, "taskname": taskname[0][0]}
        else:
            return {"fields": lst}
    except Exception as e:
        print(str(e))
        return {"fields": []}


def fn_insert_taskdata(request,decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        assigner_fk = decoded.get("emp_fk")
        taskdata = {}
        keys = []
        values = []
        for key, value in request.items():
            if key not in ['task_type', 'assignee', 'checker', 'target_date', 'remarks', 'repeat']:
                taskdata.update({key: value})
            else:
                if key == 'assignee':
                   keys.append('assignee')
                   values.append("'" + str(value['emp_details']) + "'")
                   keys.append('assignee_fk')
                   values.append(str(value['employee_fk']))
                elif key == 'checker':
                    keys.append('checker')
                    values.append("'" + str(value['emp_details']) + "'")
                    keys.append('checker_fk')
                    values.append(str(value['employee_fk']))
                elif key == 'repeat':
                    keys.append('repeat')
                    values.append("'" + str(value['repeat']) + "'")
                    keys.append('repeat_fk')
                    values.append(str(value['repeat_pk']))
                elif key == 'target_date':
                    keys.append('target_date')
                    values.append("'" + str(convert_ist_timezone(value)).split(" ")[0] + "'")
                else:
                    keys.append(key)
                    values.append("'" + str(value) + "'")
        if 'assignee_fk' in keys and 'checker_fk' in keys:
            if str(values[keys.index('assignee_fk')]) == str(values[keys.index('checker_fk')]):
                return {"message": "Assignee and checker name has to be different", "rval": 0}
            else:
                data = ','.join(values)
                qry = ("insert into Web_task_assignment(comp_fk,assigner_fk,taskupload_data," + ','.join(
                    keys) + ",dt,status) values(?,?,?," + data + ",getdate(),?)")
                values = (comp_fk, assigner_fk, str(taskdata), 1)
                py_connection.put_result(qry, values)
                return {"message": "Task Created Successfully", "rval": 1}
        else:
            data = ','.join(values)
            qry = ("insert into Web_task_assignment(comp_fk,assigner_fk,taskupload_data," + ','.join(keys) + ",dt,status) values(?,?,?," + data + ",getdate(),?)")
            values = (comp_fk,assigner_fk,str(taskdata),1)
            py_connection.put_result(qry, values)
            return {"message": "Task Created Successfully", "rval": 1}
    except Exception as e:
        print(str(e))
        return {"message": "Something Went Error ", "rval": 0}


def fn_get_taskdata(request, decoded):
    try:
        task_type = request.get("task_type")
        task_status = int(request.get("taskstatus"))
        employee_fk = decoded.get("emp_fk")
        comp_fk = decoded.get("comp_fk")
        sql_command = "{call Web_sp_gettaskdata(?,?,?,?)}"
        params = (task_type,task_status, employee_fk, comp_fk)
        result, k = py_connection.call_prop1(sql_command,params)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                view_data["Action"] = ast.literal_eval(view_data["Action"])
                for key, value in view_data["Action"].items():
                    if key.endswith("Date"):
                        view_data["Action"][key] = convert_ist_timezone(value).split(" ")[0]
                lst.append(view_data)
            return {"header": k, "reports": lst}
        else:
            return {"header": k, "reports": lst}
    except Exception as e:
        print(str(e))
        return {"header": [], "reports": []}


def fn_get_adminreport(request, decoded):
    try:
        task_type = request.get("task_type")
        stat = int(request.get("stat"))
        emp_fk = request.get("assignee_fk")
        comp_fk = decoded.get("comp_fk")
        assigner_fk = decoded.get("emp_fk")
        sql_command = "{call Web_sp_adminreport(?,?,?,?,?)}"
        params = (task_type, emp_fk, stat, assigner_fk, comp_fk)
        result, k = py_connection.call_prop1(sql_command, params)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                view_data["Data"] = ast.literal_eval(view_data["Data"])
                for key, value in view_data["Data"].items():
                    if key.endswith("Date"):
                        view_data["Data"][key] = convert_ist_timezone(value).split(" ")[0]
                lst.append(view_data)
            return {"header": k, "reports": lst}
        else:
            return {"header": k, "reports": lst}
    except Exception as e:
        print(str(e))
        return {"header": [], "reports": []}


def fn_get_employeereport(request, decoded):
    try:
        task_type = request.get("task_type")
        emp_fk = decoded.get("emp_fk")
        comp_fk = decoded.get("comp_fk")
        sql_command = "{call Web_sp_employeereport(?,?,?)}"
        params = (emp_fk, comp_fk,task_type,)
        result, k = py_connection.call_prop1(sql_command, params)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                view_data["Data"] = ast.literal_eval(view_data["Data"])
                for key, value in view_data["Data"].items():
                    if key.endswith("Date"):
                        view_data["Data"][key] = convert_ist_timezone(value).split(" ")[0]
                lst.append(view_data)
                print(lst)
            return {"header": k, "reports": lst}
        else:
            return {"header": k, "reports": lst}
    except Exception as e:
        print(str(e))
        return {"header": [], "reports": []}


def fn_get_checkerupdatestatus(request):
    try:
        task_fk = request.get("task_fk")
        task_status = request.get("status")
        remarks = request.get("remarks", '')
        sqlcommands = "{call Web_sp_checkerstatusupdate(?,?,?)}"
        params = (task_fk, task_status, remarks)
        py_connection.call_prop(sqlcommands, params)
        return {"message": "Task Rejected Successfully" if task_status == 5 else "Task Approved Successfully"}

    except Exception as e:
        print(str(e))
        return {"message": "Task Verification unsuccessfull", "rval": 0}


def fn_get_web_taskcount(decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        emp_fk = decoded.get("emp_fk")
        sql_command = "{CALL Web_sp_taskcount(?, ?)}"
        params = (emp_fk, comp_fk)
        result, k = py_connection.call_prop1(sql_command, params)
        lst = []
        open = 0
        pending = 0
        completed = 0
        rejected = 0
        review = 0
        if result and len(result) > 0:
            for row in result:
                open = open + row[1]
                pending = pending + row[2]
                completed = completed + row[3]
                rejected = rejected + row[4]
                review = review + row[5]
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"lst": lst, "all": [{'open': open, 'pending': pending, 'completed': completed, 'rejected': rejected, 'review': review}]}
    except Exception as e:
        print(str(e))


def fn_get_admin_taskcount(decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        emp_fk = decoded.get("emp_fk")
        print(emp_fk, comp_fk)
        sql_command = "{CALL Web_sp_admintaskcount(?, ?)}"
        params = (emp_fk, comp_fk)
        result, k = py_connection.call_prop1(sql_command, params)
        lst = []
        Assigned_to_Assignee = 0
        Assigned_to_Checker = 0
        completed = 0
        Rejected_by_Checker = 0
        if result and len(result) > 0:
            for row in result:
                Assigned_to_Assignee = Assigned_to_Assignee + row[1]
                Assigned_to_Checker = Assigned_to_Checker + row[2]
                completed = completed + row[3]
                Rejected_by_Checker = Rejected_by_Checker + row[4]
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"lst": lst, "all": [{'Assigned_to_Assignee': Assigned_to_Assignee, 'Assigned_to_Checker': Assigned_to_Checker, 'completed': completed, 'Rejected_by_Checker': Rejected_by_Checker}]}
    except Exception as e:
        print(str(e))


def fn_get_checker(request, decoded):
    try:
        task_type = request.get("task_type")
        task_status = int(request.get("taskstatus"))
        employee_fk = decoded.get("emp_fk")
        comp_fk = decoded.get("comp_fk")
        sql_command = "{call Web_sp_checker(?,?,?,?)}"
        params = (employee_fk, comp_fk,task_type, task_status)
        result, k = py_connection.call_prop1(sql_command, params)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                view_data["Action"] = ast.literal_eval(view_data["Action"])
                for key, value in view_data["Action"].items():
                    if key.endswith("Date"):
                        view_data["Action"][key] = convert_ist_timezone(value).split(" ")[0]
                lst.append(view_data)
            return {"header": k, "reports": lst}
        else:
            return {"header": k, "reports": lst}
    except Exception as e:
        print(str(e))
        return {"header": [], "reports": []}


def convert_ist_timezone(dt):
    date_utc = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_timezone = pytz.timezone('UTC')
    ist_timezone = pytz.timezone('Asia/Kolkata')
    date_ist = date_utc.replace(tzinfo=utc_timezone).astimezone(ist_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return date_ist


def get_encoding_filestring(request, decoded):
    try:
        comp_fk = decoded.get("comp_fk")
        doc_fk = request.get("doc_pk")
        qry = "select doc_path, access_key from web_doc_upload where doc_pk =" + str(doc_fk) + " and comp_fk=" + str(comp_fk)
        res = py_connection.get_result(qry)
        splitstring = getfile_azure_blob(str(res[0][0]), decoded, doc_fk)
        base64string = str(splitstring) + str(res[0][1])
        return {"encoding_string": base64string}
    except Exception as e:
        print(str(e))


def get_reportfile(request, decoded):
    try:
        task_fk = request.get("task_fk")
        qry = "SELECT doc_path,access_key,document_pk FROM Web_v_assigned_task WHERE doc_pk =" + str(task_fk)
        res = py_connection.get_result(qry)
        splitstring = getfile_azure_blob(str(res[0][0]), decoded, str(res[0][2]))
        base64string = str(splitstring) + str(res[0][1])
        type, data = render_pdf(base64string)
        return {"encoded_string": data, 'type': type}
    except Exception as e:
        print(str(e))


def render_pdf(base64string):
    try:
        data = base64string.split('base64,')
        if data[0].split('/')[0] == 'data:image':
            type = 'image'
            data1 = base64string
        else:
            type = 'pdf'
            data1 = data[-1]
        return type, data1
    except Exception as e:
        print(f"Error rendering PDF: {e}")
        return []

