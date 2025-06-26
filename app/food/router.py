from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.database import async_session_maker
from app.food.dao import FoodDAO
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os
from ultralytics import YOLO


router = APIRouter(prefix='/foods', tags=['Подсчет калорий по фото'])

model = YOLO("weights/best1.pt") 

def get_calories(food_name: str):
    calorie_map = {
        "oatmeal": 115,
        "apple": 95,
        "banana": 105,
        "bread": 80,
        "muffins": 220,
        "pancake": 130,
        "omelette": 120,
        "rice": 200,
        "potato wedges": 360,
        "fries": 365,
        "glazed carrot": 50,
        "macaroni": 160,
        "crusted chicken": 250,
        "cucumber": 16,
        "beet": 44,
        "sunny sideup egg": 180,
        "chicken": 230,
        "fish": 200,
        "yogurt": 120,
        "cheese": 110,
        "salad": 30,
        "avocado": 160,
        "orange": 60,
        "grapes": 70,
        "carrot": 40,
        "tomato": 20,
        "lettuce": 15
    }
    return calorie_map.get(food_name.lower(), 100)

@router.post("/predict/")
async def predict(
    file: UploadFile = File(...),
    id: int = Form(...),  # Получаем из формы
    product_name: str = Form(...)  # Получаем из формы
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
                calories = get_calories(food_type)
                await FoodDAO.add(
                    session=session,
                    id = id,
                    product_name = food_type
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