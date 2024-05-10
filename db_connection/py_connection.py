import pyodbc
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = str(Path(__file__).absolute().parents[1] / "config.env")
load_dotenv(env_path)


def get_mssql_connection():
    try:
        conn = pyodbc.connect('DRIVER={' + os.getenv("DRIVER") + '};SERVER=' + os.getenv("HOST") + ';DATABASE=' + os.getenv("DB") + ';UID=' + os.getenv("USER") +';PWD=' + os.getenv(
            "PASSWORD") + '')
        return conn
    except Exception as e:
        print("get_mssql_connection " + str(e))


def get_result(query):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(query)
    row = cursor_str.fetchall()
    mssql_conn.close()
    return row


def get_result_col(query):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(query)
    row = cursor_str.fetchall()
    column_names = [column[0] for column in cursor_str.description]
    mssql_conn.close()
    return row, column_names


def put_result(query, data):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(query, data)
    mssql_conn.commit()
    mssql_conn.close()
    return cursor_str.rowcount


def put_result1(query):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(query)
    mssql_conn.commit()
    mssql_conn.close()
    return cursor_str.rowcount


def put_result2(qry, pram):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.executemany(qry, pram)
    mssql_conn.commit()
    mssql_conn.close()
    return cursor_str.rowcount


def call_prop(qry,params):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(qry, params)
    mssql_conn.commit()
    mssql_conn.close()
    return cursor_str.rowcount


def call_prop1(qry,params):
    mssql_conn = get_mssql_connection()
    cursor_str = mssql_conn.cursor()
    cursor_str.execute(qry,params)
    row = cursor_str.fetchall()
    column_names = [column[0] for column in cursor_str.description]
    mssql_conn.close()
    return row, column_names
