import json

from mountaineer import ControllerBase, Metadata, RenderBase, sideeffect

from fastapi import Depends, Response

from everest.core.auth.dependencies import AuthDependencies
from everest.models import User


class LogoutRender(RenderBase):
    pass


class LogoutController(ControllerBase):
    url = "/logout"
    view_path = "/auth/logout/page.tsx"

    async def render(
            self,
            user=Depends(AuthDependencies.lookup_user(User)),
    ) -> LogoutRender:
        return LogoutRender(
            metadata=Metadata(title="Logout"),
        )

    @sideeffect
    async def logout(self, response: Response) -> None:
        response.headers['update-session-cookie'] = json.dumps({'user_id': None})
