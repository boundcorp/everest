from mountaineer import ControllerBase, Metadata, RenderBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from everest.core.layout import LayoutContext


class HomeRender(RenderBase):
    layout: LayoutContext


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            layout: LayoutContext = Depends(LayoutContext.get_layout),
    ) -> HomeRender:
        return HomeRender(
            layout=layout,
            metadata=Metadata(title="Home"),
        )
