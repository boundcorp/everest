from datetime import timedelta

from fastapi import Depends
from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata

from everest.controllers.app.item_create import ItemCreateController
from everest.controllers.app.item_detail import TableItemController
from everest.controllers.app.item_edit import ItemEditController
from everest.controllers.app.layout import AdminLayoutController
from everest.controllers.auth.layout import AuthLayoutController
from everest.controllers.auth.login import LoginController
from everest.controllers.app.table_list import TableListController
from everest.controllers.app.home import HomeController

from everest.config import AppConfig
from everest.controllers.auth.logout import LogoutController
from everest.logging import configure_logging

from everest.middleware import log_middleware, create_session_middleware

configure_logging()

config = AppConfig()
controller = AppController(
    config=config,

    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],
    fastapi_args={"dependencies": [Depends(log_middleware)]},

)

controller.register(AdminLayoutController())
controller.register(HomeController())
controller.register(TableListController())
controller.register(ItemEditController())
controller.register(ItemCreateController())
controller.register(TableItemController())
controller.register(AuthLayoutController())
controller.register(LoginController())
controller.register(LogoutController())

controller.app.middleware("http")(
    create_session_middleware(config.API_SECRET_KEY, config.SESSION_COOKIE_NAME,
                              session_ttl=timedelta(seconds=config.SESSION_JWT_TTL)))
