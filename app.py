from fastapi import Request, FastAPI, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse(
        name='user_age_response.html.j2',
        context={'request': request, 'name': name, 'age': age},
        status_code=status.HTTP_200_OK
    )


# Zadanie 3.3
@app.get("/info")
def info(request: Request, format=None):
    if not format:
        pass

    elif format.lower() == 'json':
        return {'user_agent': request.headers.get('User-Agent')}

    elif format.lower() == 'html':
        return templates.TemplateResponse(
            name='user_agent_response.html.j2',
            context={'request': request, 'user_agent': request.headers.get('User-Agent')}
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong format')


# Zadanie 3.4
paths = set()


@app.get('/save/{path}')
def save_get(path: str):
    if path not in paths:
        raise HTTPException(status_code=404)
    else:
        return RedirectResponse(url='/info', status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.put('/save/{path}')
def save_put(path: str):
    paths.add(path)
    return Response(status_code=status.HTTP_200_OK)


@app.delete('/save/{path}')
def save_delete(path: str):
    paths.discard(path)
    return Response(status_code=status.HTTP_200_OK)


@app.post('/save/{path}')
@app.options('/save/{path}')
@app.head('/save/{path}')
@app.trace('/save/{path}')
@app.patch('/save/{path}')
def save_other(path: str):
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
