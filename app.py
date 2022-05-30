from fastapi import Request, FastAPI, Depends, HTTPException, status
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
    return """
    <html>
        <head>
            <title>HTML</title>
        </head>
        <body>
            <h1>The unix epoch started at 1970-01-01</h1>
        </body>
    </html>
"""


# Zadanie 3.2
def fetch_user_age(birth_date_str: str) -> int:
    try:
        birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        return -1

    if birth_date > datetime.datetime.today():
        return -1

    return (datetime.datetime.today() - birth_date).days // 365


@app.post("/check", response_class=HTMLResponse)
def login(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    name = credentials.username
    age = fetch_user_age(credentials.password)

    if age < 16:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return templates.TemplateResponse(
            name='user_age_response.html.j2',
            context={'request': request, 'name': name, 'age': age},
            status_code=status.HTTP_200_OK
        )
