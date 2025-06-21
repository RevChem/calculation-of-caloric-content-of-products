from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.database import async_session_maker
from app.food.dao import FoodDAO
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os
from ultralytics import YOLO
from app.food.sql_enums import Product


router = APIRouter(prefix='/foods', tags=['Подсчет калорий по фото'])

model = YOLO("weights/best1.pt") 

@router.post("/predict/")
async def predict(
    file: UploadFile = File(...)
):
    # Проверка типа файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    # Сохраняем временный файл
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Обработка изображения
        image = Image.open(file_path)
        results = model(image)

        # Получаем уникальные классы еды (чтобы избежать дубликатов)
        class_ids = list(set(results[0].boxes.cls.int().tolist()))
        food_types = [model.names[i] for i in class_ids]

        # Конвертируем изображение с результатами
        plotted_img = results[0].plot()
        img_bytes = io.BytesIO()
        Image.fromarray(plotted_img[..., ::-1].copy()).save(img_bytes, format="JPEG")

        # Сохраняем данные в БД
        async with async_session_maker() as session:
            for food_type in food_types:
                calories = Product.get_calories(food_type)
                await FoodDAO.add(
                    product_name = food_type,
                    calories = calories
                )
            await session.commit()

        return StreamingResponse(
            io.BytesIO(img_bytes.getvalue()),
            media_type="image/jpeg",
            headers={"X-Food-Types": ", ".join(food_types)}  # Дополнительная информация в headers
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Удаляем временный файл в любом случае
        if os.path.exists(file_path):
            os.remove(file_path)