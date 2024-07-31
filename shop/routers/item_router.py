from fastapi import APIRouter
from shop.data_base import items, database
from shop.models import Item, ItemIn
from typing import List

router = APIRouter()


@router.get('/items', response_model=List[Item])
async def get_items():
    query = items.select()
    return await database.fetch_all(query)


@router.get('/items/{item_id}', response_model=Item)
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    return await database.fetch_one(query)


@router.post('/items', response_model=ItemIn)
async def create_item(new_item: ItemIn):
    query = items.insert().values(
        name=new_item.name,
        description=new_item.description,
        price=new_item.price
    )
    await database.execute(query)
    return new_item


@router.put('/items/{item_id}', response_model=ItemIn)
async def update_item(item_id: int, new_item: ItemIn):
    query = items.update().where(items.c.id == item_id).values(**new_item.dict())
    await database.execute(query)
    return new_item


@router.delete('/items/{item_id}', response_model=dict)
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'item deleted'}


@router.get("/fake_items/{count}", response_model=dict)
async def create_fake_items(count: int):
    for i in range(1, count + 1):
        query = items.insert().values(name=f'name_{i}',
                                      description=f'description_{i}',
                                      price=i,
                                      )
        await database.execute(query)

    return {'message': f'{count} fake items create'}
