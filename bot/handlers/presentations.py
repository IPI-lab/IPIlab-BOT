from aiogram import Router, types

from bot.keyboards import main_kb

router = Router()


@router.message(
    lambda message: message.text == "/presentations" or message.text == "Презентации 📊"
)
async def cmd_resouces(message: types.Message):
    await message.answer(
        "Раздел с презентациями еще в разработке!",
        reply_markup=main_kb,
    )
