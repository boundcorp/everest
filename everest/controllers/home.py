from mountaineer import ControllerBase, Metadata, RenderBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from everest.core.layout import LayoutContext
from everest.core.tables import ALL_TABLES


class HomeRender(RenderBase):
    layout: LayoutContext


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ) -> HomeRender:
        layout = LayoutContext(tables=ALL_TABLES())
        return HomeRender(
            layout=layout,
            metadata=Metadata(title="Home"),
        )
