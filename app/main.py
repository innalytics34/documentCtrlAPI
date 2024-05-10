import pyodbc
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run
from fastapi import FastAPI, Request, HTTPException, Depends,Cookie
import json
from auth import py_jwt
from doc_upload import py_doc_upload
from filter import py_filter
from login import py_login
from dashboard import dashboard
from pydantic import BaseModel
from fastapi.responses import FileResponse
# from a2wsgi import ASGIMiddleware

auth_scheme = py_jwt.JWTBearer()

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "success"}


@app.post("/IEC/login")
async def login(request: Request):
    try:
        request = await request.json()
        response = py_login.fn_login(request)
        return response
    except Exception as e:
        print(str(e))


@app.post("/IEC/doc_upload")
async def doc_upload(request: Request,decoded: dict = Depends(auth_scheme)):
    try:
         if decoded:
            request = await request.json()
            response = py_doc_upload.fn_doc_upload(request, decoded)
            return response
         else:
           raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
         print(str(e))


@app.get("/IEC/webtaskcount")
async def webtaskcount(decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            response = dashboard.fn_get_web_taskcount(decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
         print(str(e))


@app.get("/IEC/admintaskcount")
async def adminwebtaskcount(decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            response = dashboard.fn_get_admin_taskcount(decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
         print(str(e))

@app.get("/IEC/encoding_string")
async def encoding_string(data: str = {"doc_pk": "12"}, decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            request = json.loads(data)
            response = dashboard.get_encoding_filestring(request, decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))


@app.get("/IEC/task_list")
def task_list(decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            response = py_filter.get_tasklist()
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
         print(str(e))


@app.get("/IEC/taskstatuslist")
def taskstatuslist(decoded: dict = Depends(auth_scheme)):
    try:
         if decoded:
            response = py_filter.get_taskstatus()
            return response
         else:
             raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
         print(str(e))

@app.get("/IEC/repeat_list")
async def repeat_list(decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            response = py_filter.get_repeatlst()
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))

@app.get("/IEC/emp_list")
def emp_list():
    try:
        response = py_filter.get_emplist()
        return response
    except Exception as e:
        print(str(e))


@app.get("/IEC/emp_details_list")
def emp_details_list():
    try:
        response = py_filter.get_emp_details()
        return response
    except Exception as e:
        print(str(e))

@app.get("/IEC/get_fields")
async def get_fields(data : str = {"task_type" : 1}):
    try:
        request = json.loads(data)
        print(request)
        response = dashboard.get_inputfield(request)
        print(response)
        return response
    except Exception as e:
        print(str(e))

@app.post("/IEC/insert_task")
async def insert_task(request: Request, decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            request = await request.json()
            print(request)
            response = dashboard.fn_insert_taskdata(request, decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))


@app.get("/IEC/get_taskdata")
async def get_taskdata(data : str ={"emp_fk":" ","task_type" : " ","task_status": " "},  decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            request = json.loads(data)
            print(request)
            response = dashboard.fn_get_taskdata(request,decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))


@app.get("/IEC/get_checkerdata")
async def get_taskdata(data : str ={"emp_fk":" ","task_type" : " ","task_status": " "},  decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            request = json.loads(data)
            print(request)
            response = dashboard.fn_get_checker(request,decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))


@app.get("/IEC/get_reportfile")
async def get_reportfile(data: str = '{"task_fk": ""}', decoded: dict = Depends(auth_scheme)):
    try:
         if decoded:
            request = json.loads(data)
            response = dashboard.get_reportfile(request, decoded)
            return response
         else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")

    except Exception as e:
        print(str(e))


@app.post("/IEC/checkerupdatestatus")
async def get_checkerupdatestatus(request: Request, decoded: dict = Depends(auth_scheme)):
    try:
        if decoded:
            request = await request.json()
            print(request)
            response = dashboard.fn_get_checkerupdatestatus(request)
            print(response)
            return response
    except Exception as e:
        print(str(e))


@app.get("/IEC/statusname")
async def statusname(decoded = Depends(auth_scheme)):
    try:
        if decoded:
            response = py_filter.get_task_status()
            return response
    except Exception as e:
        print(str(e))

@app.get("/IEC/adminreport")
async def get_adminreport(data: str = {"task_type" : "0","stat" : "0", "emp_fk": "1000183"}, decoded = Depends(auth_scheme)):
    try:
        if decoded:
            request = json.loads(data)
            print(request)
            response = dashboard.fn_get_adminreport(request,decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
        print(str(e))

@app.get("/IEC/employeereport")
async def get_employeereport(data: str = {"task_type" : "0"}, decoded=Depends(auth_scheme)):
    try:
        if decoded:
            request = json.loads(data)
            print(request)
            response = dashboard.fn_get_employeereport(request,decoded)
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")
    except Exception as e:
        print(str(e))


# # wsgi_app = ASGIMiddleware(app)
#
# if __name__ == "__main__":
#     run(app, host="0.0.0.0", port=805)

