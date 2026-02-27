from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

from app.database import AsyncSessionLocal
from app.models import StationTask
from app.services.task_sync import sync_tasks


app = FastAPI()

# -----------------------------
# STATIC FILES
# -----------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# -----------------------------
# TEMPLATES
# -----------------------------
templates = Jinja2Templates(directory="app/templates")


# -----------------------------
# DB dependency
# -----------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# -----------------------------
# Background sync (каждые 30 сек)
# -----------------------------
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_sync())


async def background_sync():
    while True:
        try:
            print("BACKGROUND: sync start")
            await sync_tasks()
            print("BACKGROUND: sync done")
        except Exception as e:
            print("Sync error:", e)

        await asyncio.sleep(30)


# -----------------------------
# UI
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(StationTask).order_by(StationTask.id.asc())
    )
    tasks = result.scalars().all()

    return templates.TemplateResponse(
        "station/index.html",
        {
            "request": request,
            "tasks": tasks
        }
    )