from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки
button_search = KeyboardButton(text="Поиск статей 🔍")
button_help = KeyboardButton(text="Помощь 🆘")
button_videos = KeyboardButton(text="Поиск по видео 🎥")
button_resources = KeyboardButton(text="Ресурсы компании 📚")
button_presentations = KeyboardButton(text="Презентации 📊")

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_search],
        [button_help, button_videos],
        [button_resources, button_presentations],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# Клавиатура с кнопкой "Назад"
back_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад ◀️")]],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# Клавиатура для выбора категорий поиска
search_categories_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="BusinessChain"),
            KeyboardButton(text="MakeEvents"),
        ],
        [
            KeyboardButton(text="ELK"),
            KeyboardButton(text="HRChain"),
        ],
        [KeyboardButton(text="Назад ◀️")],
    ],
    resize_keyboard=True,
)

if __name__ == "__main__":
    print("You must use main.py")
