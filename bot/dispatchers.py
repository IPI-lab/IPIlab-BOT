from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .handlers import start, help, search, videos, resources, presentations, unknown


def setup_dp() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(search.router)
    dp.include_router(videos.router)
    dp.include_router(resources.router)
    dp.include_router(presentations.router)
    dp.include_router(unknown.router)

    return dp


if __name__ == "__main__":
    print("You must use main.py")
