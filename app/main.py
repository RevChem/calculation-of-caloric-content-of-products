from fastapi import FastAPI

from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.pages.router import router as router_pages
from app.food.router import router as router_foods
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_pages)
app.include_router(router_foods)
