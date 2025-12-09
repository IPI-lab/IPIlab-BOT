from .start import router as start_router
from .help import router as help_router
from .search import router as search_router
from .videos import router as videos_router
from .unknown import router as unknow_router
from .resources import router as resources_router
from .presentations import router as presentations_router

__all__ = [
    "start_router",
    "help_router",
    "search_router",
    "videos_router",
    "unknow_router",
    "resources_router",
    "presentations_router",
]
