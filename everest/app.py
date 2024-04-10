import json

from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata

from everest.controllers.table_item import TableItemController
from everest.controllers.table_list import TableListController
from everest.controllers.home import HomeController

from everest.config import AppConfig
from everest.core.jwt import create_session_middleware
from fastapi.responses import Response
from fastapi.requests import Request

config = AppConfig()
controller = AppController(
    config=config,

    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],

)

controller.register(HomeController())
controller.register(TableListController())
controller.register(TableItemController())

controller.app.middleware("http")(create_session_middleware(config.API_SECRET_KEY, config.SESSION_COOKIE_NAME))


@controller.app.get("/login")
async def login(request: Request, response: Response):
    existing = getattr(request, "session_cookie", {})
    existing.update({"user_id": "dfa55fe4-017f-4b97-a545-45c6035e28bd"})
    response.headers["update-session-cookie"] = json.dumps(existing)
    return {"ok": "good"}
