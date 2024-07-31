import uvicorn
from fastapi import FastAPI
from data_base import database
from routers.user_router import router as router_user
from routers.item_router import router as router_item
from routers.order_router import router as router_order


app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(router_user, tags=['users'])
app.include_router(router_item, tags=['items'])
app.include_router(router_order, tags=['orders'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
