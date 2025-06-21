from fastapi import FastAPI

from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.pages.router import router as router_pages
from app.food.router import router as router_foods
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import asyncio
from faststream import FastStream
from config import scheduler, broker
from routers.router_tasks import router as router_task
from routers.router_scheduler import router as router_scheduler
from loguru import logger


app = FastStream(broker)


@app.after_startup
async def startup_tasks():
    logger.info("FastStream успешно запущен, планировщик задач инициализируется...")
    scheduler.start()


@app.after_shutdown
async def shutdown_tasks():
    logger.info("Останавливаю планировщик задач...")

    # Удаляем все задачи из планировщика
    scheduler.remove_all_jobs()

    # Останавливаем планировщик
    scheduler.shutdown()


async def register_app():
    broker.include_router(router_task)
    broker.include_router(router_scheduler)
    await app.run()


app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_pages)
app.include_router(router_foods)


if __name__ == '__main__':
    try:
        asyncio.run(register_app())
    except KeyboardInterrupt:
        logger.info("Остановка приложения...")