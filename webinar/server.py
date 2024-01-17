import json

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, User, engine, init_orm

app = web.Application()


async def hash_password(password: str):
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


async def init_db(app: web.Application):
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(init_db)
app.middlewares.append(session_middleware)


def get_http_error(error_class, message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


async def get_user_by_id(session: Session, user_id: int):
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, f"User with id {user_id} not found")
    return user


async def add_user(session: Session, user: User):
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        raise get_http_error(
            web.HTTPConflict, f"User with name {user.name} already exists"
        )
    return user


class UserView(web.View):
    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get_user(self):
        return await get_user_by_id(self.session, self.user_id)

    async def get(self):
        user = await self.get_user()
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        user = User(**json_data)
        await add_user(self.session, user)
        return web.json_response({"id": user.id})

    async def patch(self):
        json_data = await self.request.json()
        user = await self.get_user()
        for field, value in json_data.items():
            setattr(user, field, value)
        await add_user(self.session, user)
        return web.json_response(user.dict)

    async def delete(self):
        user = await self.get_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/user/{user_id:\d+}", UserView),
        web.patch("/user/{user_id:\d+}", UserView),
        web.delete("/user/{user_id:\d+}", UserView),
        web.post("/user", UserView),
    ]
)

web.run_app(app, port=8080)
