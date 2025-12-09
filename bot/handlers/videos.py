from aiogram import Router, types

router = Router()


@router.message(
    lambda message: message.text == "/videos" or message.text == "Поиск по видео 🎥"
)
async def cmd_videos(message: types.Message):
    await message.answer(
        "🎥 Поиск видео пока в разработке.\nСледите за обновлениями в канале: @ipe_news"
    )


if __name__ == "__main__":
    print("You must use main.py")
