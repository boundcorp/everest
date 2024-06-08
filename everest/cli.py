import asyncio
import sys

from click import command, option
from mountaineer.cli import handle_runserver, handle_watch, handle_build, import_from_string
from mountaineer.database.cli import handle_createdb
from mountaineer.database.dependencies.core import engine_from_config
from mountaineer.io import async_to_sync
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from everest import models
from everest.config import AppConfig


@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="everest",
        webservice="everest.main:app",
        webcontroller="everest.app:controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="everest",
        webcontroller="everest.app:controller",
    )


@command()
def build():
    handle_build(
        webcontroller="everest.app:controller",
    )


def db_helper(engine):
    maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    class DBHelper:
        def __init__(self):
            self.maker = maker
            self.engine = engine

        async def aquery(self, q):
            async with self.maker() as session:
                return await session.execute(q)

        async def asave(self, *args):
            async with self.maker() as session:
                for arg in args:
                    session.add(arg)
                await session.commit()

        async def adelete(self, *args):
            async with self.maker() as session:
                for arg in args:
                    await session.delete(arg)
                await session.commit()

        def query(self, q):
            return asyncio.get_event_loop().run_until_complete(self.aquery(q))

        def save(self, *args):
            return asyncio.get_event_loop().run_until_complete(self.asave(*args))

        def delete(self, *args):
            return asyncio.get_event_loop().run_until_complete(self.adelete(*args))

    return DBHelper()


@command()
def shell():
    config = import_from_string("everest.config:AppConfig")()

    # Simplified helper to run async functions
    def wait(coroutine):
        return asyncio.get_event_loop().run_until_complete(coroutine)

    # Modified to directly use config without FastAPI dependency injection
    engine = engine_from_config(config)
    db = db_helper(engine)
    from everest.app import controller

    # Open bpython with injected locals
    try:
        from bpython.curtsies import main as bpythonEmbed
        bpythonEmbed(locals_=dict(
            config=config,
            engine=engine,
            select=select,
            controller=controller,
            models=models,
            wait=wait,
            db=db,
        ))
    except ImportError:
        raise ImportError("bpython is required for the shell command")


@command()
def worker():
    config = import_from_string("everest.config:AppConfig")()

    # Modified to directly use config without FastAPI dependency injection
    engine = engine_from_config(config)
    db = db_helper(engine)



@command()
@async_to_sync
async def createdb():
    _ = AppConfig()

    await handle_createdb(models)


if __name__ == "__main__":
    if sys.argv[1] == "runserver":
        runserver()

    if sys.argv[1] == "shell":
        shell()
