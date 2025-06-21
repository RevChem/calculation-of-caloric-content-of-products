from enum import Enum

class Product(Enum):
    OATMEAL = 115
    APPLE = 95
    BANANA = 105
    BREAD = 80
    MUFFINS = 220
    PANCAKE = 130
    OMELETTE = 120
    RICE = 200
    POTATO_WEDGES = 360
    FRIES = 365
    GLAZED_CARROT = 50
    MACARONI = 160
    CRUSTED_CHICKEN = 250
    CUCUMBER = 16
    BEET = 44
    SUNNY_SIDEUP_EGG = 180
    CHICKEN = 230
    FISH = 200
    YOGURT = 120
    CHEESE = 110
    SALAD = 30
    AVOCADO = 160
    ORANGE = 60
    GRAPES = 70
    CARROT = 40
    TOMATO = 20
    LETTUCE = 15

    @classmethod
    def get_calories(cls, food_name: str, default: int = 100) -> int:
        try:
            return cls[food_name.upper()].value
        except KeyError:
            return default