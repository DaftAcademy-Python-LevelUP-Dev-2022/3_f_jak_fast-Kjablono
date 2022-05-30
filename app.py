from fastapi import Request, FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Zadanie 3.1
@app.get("/start")
def read_unix_epoch():
    return """
    <html>
        <head>
            <title>HTML</title>
        <head>
        <body>
            <h1>The unix epoch started at 1970-01-01</h1>
        </body>
    </html>
    """