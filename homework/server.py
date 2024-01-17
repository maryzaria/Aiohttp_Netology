import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement, engine, init_orm

app = web.Application()


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


async def get_advert_by_id(session: Session, adv_id: int):
    advertisement = await session.get(Advertisement, adv_id)
    if advertisement is None:
        raise get_http_error(
            web.HTTPNotFound, f"Advertisement with id = {adv_id} not found"
        )
    return advertisement


async def add_advert(session: Session, advert: Advertisement):
    try:
        session.add(advert)
        await session.commit()
    except IntegrityError:
        raise get_http_error(
            web.HTTPConflict,
            f"Advertisement with title '{advert.title}' already exists",
        )
    return advert


class AdvertisementView(web.View):
    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def adv_id(self):
        return int(self.request.match_info["adv_id"])

    async def get_adv(self):
        return await get_advert_by_id(self.session, self.adv_id)

    async def get(self):
        advert = await self.get_adv()
        return web.json_response(advert.dict)

    async def post(self):
        json_data = await self.request.json()
        advert = Advertisement(**json_data)
        await add_advert(self.session, advert)
        return web.json_response({"id": advert.id})

    async def patch(self):
        json_data = await self.request.json()
        advert = await self.get_adv()
        for field, value in json_data.items():
            setattr(advert, field, value)
        await add_advert(self.session, advert)
        return web.json_response(advert.dict)

    async def delete(self):
        advert = await self.get_adv()
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/advert/{adv_id:\d+}", AdvertisementView),
        web.patch("/advert/{adv_id:\d+}", AdvertisementView),
        web.delete("/advert/{adv_id:\d+}", AdvertisementView),
        web.post("/advert", AdvertisementView),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)
