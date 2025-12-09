from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ..config import MAINPAGE_URLS
from ..utils.text_utils import split_text, split_md, create_clickable_links
from ..utils import (
    query_n8n,
    query_businesschain,
    query_makeevents,
    query_elk,
    query_hrchain,
)
from bot.keyboards import back_kb, main_kb, search_categories_kb

router = Router()


class SearchState(StatesGroup):
    waiting_for_category = State()
    waiting_for_query = State()


@router.message(
    lambda message: message.text == "/search" or message.text == "Поиск статей 🔍"
)
async def cmd_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_category)
    await message.answer(
        "Выберите категорию для поиска:", reply_markup=search_categories_kb
    )


@router.message(SearchState.waiting_for_category, F.text == "Назад ◀️")
async def cancel_search_from_category(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Поиск отменён.", reply_markup=main_kb)


@router.message(SearchState.waiting_for_category, F.text)
async def handle_search_category(message: types.Message, state: FSMContext):
    category = message.text.strip()

    # Сохраняем выбранную категорию и переходим к вводу запроса
    await state.update_data(category=category)
    await state.set_state(SearchState.waiting_for_query)

    await message.answer(
        f"Выбрана категория: [{category}]({MAINPAGE_URLS[category]})\nВведите текст для поиска:",
        reply_markup=back_kb,
        parse_mode="MarkDownV2",
    )


@router.message(SearchState.waiting_for_query, F.text == "Назад ◀️")
async def cancel_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_category)
    await message.answer(
        "Выберите категорию для поиска:", reply_markup=search_categories_kb
    )


@router.message(SearchState.waiting_for_query, F.text)
async def handle_search_query(message: types.Message, state: FSMContext):
    query = message.text.strip()
    user_data = await state.get_data()
    category = user_data.get("category", "")

    print(f"DEBUG: Search query '{query}' in category '{category}'")

    if not query:
        await message.answer("❌ Запрос не может быть пустым.")
        return

    # Перенаправление на соответствующие обработчики в зависимости от категории
    category_clean = category.strip().lower()

    if category_clean == "businesschain":
        await search_businesschain(message, query, state)
    elif category_clean == "makeevents":
        await search_makeevents(message, query, state)
    elif category_clean == "elk":
        await search_elk(message, query, state)
    elif category_clean == "hrchain":
        await search_hrchain(message, query, state)
    else:
        await message.answer("❌ Неизвестная категория поиска.")


async def universal_search_handler(
    message: types.Message, query: str, system_name: str, query_function: callable
):
    """Универсальный обработчик поиска для всех систем"""
    try:
        result = await query_function(query, message.from_user.id, message.chat.id)

        print(f"DEBUG: {system_name} result: {result}")  # Для отладки

        if not result:
            await message.answer(
                f"По вашему запросу в {system_name} ничего не найдено. 🥲"
            )
            return

        if "error" in result:
            error_info = (
                result.get("message")
                or result.get("text")
                or result.get("exception")
                or result.get("error")
                or "Неизвестная ошибка"
            )
            await message.answer(
                f"❌ Ошибка при поиске в {system_name}:\n\n<pre>{error_info}</pre>",
            )
            return

        # Стандартные тексты для разных систем
        default_messages = {
            "BusinessChain": "По вашему запросу в BusinessChain ничего не найдено.",
            "MakeEvents": "По вашему запросу в MakeEvents ничего не найдено.",
            "ELK": "По вашему запросу в ELK ничего не найдено.",
            "HRChain": "По вашему запросу в HRChain ничего не найдено.",
        }

        response_text = result.get(
            "result", default_messages.get(system_name, "Ничего не найдено.")
        )
        await send_search_results(message, response_text, system_name)

    except Exception as e:
        print(f"ERROR in {system_name} search: {e}")
        await message.answer(
            f"❌ Произошла ошибка при поиске в {system_name}: {str(e)}"
        )


# Специализированные обработчики поиска
async def search_businesschain(message: types.Message, query: str, state: FSMContext):
    """Поиск в BusinessChain"""
    await universal_search_handler(message, query, "BusinessChain", query_businesschain)


async def search_makeevents(message: types.Message, query: str, state: FSMContext):
    """Поиск в MakeEvents"""
    await universal_search_handler(message, query, "MakeEvents", query_makeevents)


async def search_elk(message: types.Message, query: str, state: FSMContext):
    """Поиск в ЕЛК"""
    await universal_search_handler(message, query, "ELK", query_elk)


async def search_hrchain(message: types.Message, query: str, state: FSMContext):
    """Поиск в HRChain"""
    await universal_search_handler(message, query, "HRChain", query_hrchain)


async def send_search_results(
    message: types.Message, response_text: str, category_name: str
):
    """Универсальная функция для отправки результатов поиска"""
    if not response_text.strip():
        response_text = "По вашему запросу ничего не найдено. 🥲"

    await message.answer(
        f"Вот что я нашел в [{category_name}]({MAINPAGE_URLS[category_name]}) по вашему запросу 🔍\n",
        parse_mode="MarkDownV2",
    )

    for part in split_text(response_text):
        formatted_text = create_clickable_links(part)

    await message.answer(
        formatted_text,
        parse_mode="HTML",
    )


if __name__ == "__main__":
    print("You must use main.py")
