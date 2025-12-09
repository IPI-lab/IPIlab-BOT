from aiogram import Router, types, F

router = Router()


@router.message(F.text)  # Только текстовые сообщения
async def handle_unknown_message(message: types.Message):
    await message.answer(
        "Боюсь такой команды нет(\n"
        "Используй /help, чтобы посмотреть список доступных функций."
    )


if __name__ == "__main__":
    print("You must use main.py")
