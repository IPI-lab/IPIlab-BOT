from aiogram import Router, types
from bot.keyboards import main_kb

router = Router()


@router.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! 👋 Я IPE FAQ Бот. Напиши /help, чтобы узнать, что я умею.",
        reply_markup=main_kb,
    )


if __name__ == "__main__":
    print("You must use main.py")
