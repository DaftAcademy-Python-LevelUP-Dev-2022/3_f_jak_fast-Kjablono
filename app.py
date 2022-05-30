from fastapi import Request, FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.templating import Jinja2Templates

import datetime

app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")


# Zadanie 3.1
@app.get("/start", response_class=HTMLResponse)
def read_unix_epoch():
    return templates.TemplateResponse(name='start.html', context=dict())


# Zadanie 3.2
def fetch_user_age(birth_date_str: str) -> int:
    try:
        birth_date = datetime.datetime.strptime(birth_date_str, format="%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=401)

    if birth_date > datetime.datetime.today():
        raise HTTPException(status_code=401)

    return (datetime.datetime.today() - birth_date).days // 365


@app.post("/check", response_class=HTMLResponse)
def login(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    name = credentials.username
    age = fetch_user_age(credentials.password)

    if age < 16:
        return HTTPException(status_code=401)
    else:
        return templates.TemplateResponse(name='user_age_response.html', context={'name': name, 'age': age})
