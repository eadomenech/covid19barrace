from datetime import date

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.staticfiles import StaticFiles

from tasks import build


app = FastAPI()
app.mount("/download", StaticFiles(directory="download"), name="download")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/build")
async def build_gifs():
    try:
        with open('download/update.txt') as f:
            update = date.fromisoformat(f.read())
            if date.today() > update:
                build.delay()
                return {"message": "Updating gifs"}
    except:
        build.delay()
        return {"message": "Updating gifs"}
    return {"message": "Updated gifs"}

@app.get('/download/<path:filename>')
async def download(filename):
    return StaticFiles('download/confirmed.gif')
