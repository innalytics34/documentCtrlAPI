from db_connection import py_connection


def get_emplist():
    try:
        qry = "select employee_fk,name from web_v_logins where status = 1"
        result, k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"emp_lst": lst}
        else:
            return {"emp_lst": []}
    except Exception as e:
        print(str(e))

def get_emp_details():
    try:
        qry = "select employee_fk,emp_details as emp_details from web_v_logins where status = 1"
        result, k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"emp_lst": lst}
        else:
            return {"emp_lst": []}
    except Exception as e:
        print(str(e))



def get_tasklist():
    try:
        qry = "select tasklist_pk,name from web_tasklist"
        result, k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"task_lst": lst}
        else:
            return {"task_lst": []}
    except Exception as e:
        print(str(e))

def get_taskstatus():
    try:
        qry = " select ts_pk,ts_name from web_taskandstatus where status = 1 "
        result, k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"ts_lst": lst}
        else:
            return {"ts_lst": []}
    except Exception as e:
        print(str(e))

def get_repeatlst():
    try:
        qry = "select repeat,repeat_pk from Web_repeattask"
        result,k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k,row))
                lst.append(view_data)
            return{"repeat_lst": lst}
        else:
            return {"repeat_lst": []}

    except Exception as e:
        print(str(e))


def get_task_status():
    try:
        qry = " select status_pk,status_name from web_taskstatus where status = 1 "
        print(qry)
        result, k = py_connection.get_result_col(qry)
        print(result,k)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)
            return {"sts_lst": lst}
        else:
            return {"sts_lst": []}
    except Exception as e:
        print(str(e))
