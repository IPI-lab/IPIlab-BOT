from aiogram import Router, types

from ..config import MAINPAGE_URLS
from ..utils.text_utils import resources_list
from bot.keyboards import main_kb

router = Router()


@router.message(
    lambda message: message.text == "/resouces" or message.text == "Ресурсы компании 📚"
)
async def cmd_resouces(message: types.Message):
    resources = resources_list(MAINPAGE_URLS)
    await message.answer(
        f"Список наших ресурсов:\n\n{resources}",
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=main_kb,
    )
