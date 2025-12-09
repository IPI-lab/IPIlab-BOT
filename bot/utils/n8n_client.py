import aiohttp
from typing import Dict, Any

from ..config import (
    N8N_WEBHOOK_BCH_URL_PROD,
    N8N_WEBHOOK_ME_URL_PROD,
    N8N_WEBHOOK_ELK_URL_PROD,
    N8N_WEBHOOK_HRCH_URL_PROD,
    N8N_WEBHOOK_BCH_URL_TEST,
    N8N_WEBHOOK_ME_URL_TEST,
    N8N_WEBHOOK_ELK_URL_TEST,
    N8N_WEBHOOK_HRCH_URL_TEST,
)


async def query_n8n(
    query: str,
    user_id: int,
    chat_id: int,
    category: str = None,
    test_mode: bool = False,
) -> Dict[str, Any]:
    """
    Выполняет запрос к n8n вебхуку в зависимости от категории поиска

    Args:
        query: Поисковый запрос
        user_id: ID пользователя
        chat_id: ID чата
        category: Категория поиска ('businesschain', 'makeevents', 'elk', 'hrchain')
        test_mode: Использовать тестовые вебхуки если True
    """
    # Определяем URL в зависимости от категории и режима
    webhook_urls = {
        "businesschain": N8N_WEBHOOK_BCH_URL_TEST
        if test_mode
        else N8N_WEBHOOK_BCH_URL_PROD,
        "makeevents": N8N_WEBHOOK_ME_URL_TEST if test_mode else N8N_WEBHOOK_ME_URL_PROD,
        "elk": N8N_WEBHOOK_ELK_URL_TEST if test_mode else N8N_WEBHOOK_ELK_URL_PROD,
        "hrchain": N8N_WEBHOOK_HRCH_URL_TEST
        if test_mode
        else N8N_WEBHOOK_HRCH_URL_PROD,
    }

    if category not in webhook_urls:
        return {"error": True, "message": f"Unknown category: {category}"}

    url = webhook_urls[category]
    payload = {
        "query": query,
        "user_id": user_id,
        "chat_id": chat_id,
        "category": category,
        "test_mode": test_mode,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    text = await resp.text()
                    return {
                        "error": True,
                        "status": resp.status,
                        "text": text,
                        "category": category,
                    }
    except Exception as e:
        return {"error": True, "exception": str(e), "category": category}


# Альтернативные функции для удобства
async def query_businesschain(
    query: str, user_id: int, chat_id: int, test_mode: bool = False
) -> Dict[str, Any]:
    """Специализированная функция для поиска в BusinessChain"""
    return await query_n8n(query, user_id, chat_id, "businesschain", test_mode)


async def query_makeevents(
    query: str, user_id: int, chat_id: int, test_mode: bool = False
) -> Dict[str, Any]:
    """Специализированная функция для поиска в MakeEvents"""
    return await query_n8n(query, user_id, chat_id, "makeevents", test_mode)


async def query_elk(
    query: str, user_id: int, chat_id: int, test_mode: bool = False
) -> Dict[str, Any]:
    """Специализированная функция для поиска в ELK"""
    return await query_n8n(query, user_id, chat_id, "elk", test_mode)


async def query_hrchain(
    query: str, user_id: int, chat_id: int, test_mode: bool = False
) -> Dict[str, Any]:
    """Специализированная функция для поиска в HRChain"""
    return await query_n8n(query, user_id, chat_id, "hrchain", test_mode)


if __name__ == "__main__":
    print("You must use main.py")
