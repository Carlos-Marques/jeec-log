import asyncio
import time

import jwt

from dotenv import dotenv_values
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from models.logs import Logs, Base

config = dotenv_values(".env")

async def clear_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_health_handler(request):
    return web.Response(text="Alive")

async def post_log_handler(request):
    data = await request.json()
    
    jwt_token = data["jwt_token"]
    try:
        decoded = jwt.decode(jwt_token, request.app["jwt_secret"], algorithms=["HS256"])
        user_id = decoded["user_id"]
    except:
        return web.Response(status=401)

    entrypoint= data["entrypoint"]

    session = request.app["session"]
    async with session.begin():
        session.add_all(
            [
                Logs(user_id=user_id, entrypoint=entrypoint)
            ]
        )
    return web.Response()

async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg:"+config["DATABASE_URL"],
        echo=False,
        pool_size=10,
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession
    )

    async with async_session() as session:
        app = web.Application()
        app["session"] = session
        app["jwt_secret"] = config["JWT_SECRET"]
        app.add_routes([
            web.get('/', get_health_handler),
            web.post('/', post_log_handler)
            ])

        return app

web.run_app(async_main())