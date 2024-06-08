import json
import urllib
from datetime import timedelta, datetime, timezone
from uuid import uuid4

import sqlalchemy
import urllib3
from fastapi import Depends
from httpcore import URL
from jose import JWTError
from mountaineer.database import DatabaseDependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from everest.core.auth.dependencies import AuthDependencies
from everest.core.jwt import decode_data, sign_data
from everest.models import User

import logging

from everest.models.visits import Session, Visit

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


async def log_middleware(request: Request,
                         db: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                         user: User = Depends(AuthDependencies.lookup_user(User))
                         ):
    session_args = request.state.session_cookie or {}
    session_id = session_args.get("session_id", "")
    url = request.url.path
    if request.query_params:
        url += "?" + urllib.parse.urlencode(request.query_params)

    log.info(f"[{request.method}] <{user and user.username or 'Anon'}> {url}")
    now = datetime.now()
    if session_id:
        try:
            session = (await db.execute(
                select(Session).filter(Session.id == session_id))).scalars().one()
            session.updated_at = now
            db.add(session)
        except sqlalchemy.exc.NoResultFound:
            session = Session(id=session_id, user_id=user.id, created_at=now, updated_at=now)
            db.add(session)

    visit = Visit(session_id=session_id, user_id=user.id, ip=request.client.host, page=url,
                  method=request.method, created_at=now, updated_at=now)
    db.add(visit)
    await db.commit()

    # existing = await session.execute(
    # select(Session).filter(Session.id == request.state.session_cookie.get("session_id", "")))
    # try:
    # view = existing.scalars().one()
    # except sqlalchemy.exc.NoResultFound:
    # view = TableView(table=table.name, stub="default", description="Default view")
    # session.add(view)
    # await session.commit()
    # print(view)


def create_session_middleware(secret_key: str, session_cookie_name: str = "evsession", session_ttl=timedelta(days=30)):
    async def session_middleware(request: Request, handler):
        try:
            token = decode_data(secret_key, request.cookies.get(session_cookie_name))
            if not token or "session_id" not in token:
                log.warning("No token found in cookies %s" % request.cookies)
                raise JWTError
        except (JWTError, AttributeError) as e:
            log.warning("Invalid Token: %s" % e)
            token = {"session_id": str(uuid4())}

        request.state.session_cookie = token

        response: Response = await handler(request)

        update = response.headers.get("update-session-cookie", "{}")
        if update:
            try:
                token.update(json.loads(update))
            except json.JSONDecodeError:
                print("[session_middleware]: Failed to decode update session cookie")

        response.set_cookie(key=session_cookie_name, value=sign_data(secret_key, token, expires_delta=session_ttl),
                            httponly=True,
                            samesite="strict",
                            expires=datetime.now(timezone.utc) + session_ttl)
        return response

    return session_middleware
