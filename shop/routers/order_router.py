import random

from fastapi import APIRouter
from shop.data_base import orders, users, items, database
from shop.models import Order, OrderIn
from typing import List

router = APIRouter()


@router.get('/orders', response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router.get('/orders/{order_id}', response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@router.post('/orders', response_model=OrderIn)
async def create_order(new_order: OrderIn):
    query = orders.insert().values(
        items=new_order.items,
        user=new_order.user,
    )
    await database.execute(query)
    return new_order


@router.put('/orders/{order_id}', response_model=OrderIn)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return new_order


@router.delete('/orders/{order_id}', response_model=dict)
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'order deleted'}
