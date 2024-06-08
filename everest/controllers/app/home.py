from mountaineer import ControllerBase, Metadata, RenderBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class HomeRender(RenderBase):
    pass


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ) -> HomeRender:
        return HomeRender(
            metadata=Metadata(title="Home"),
        )
