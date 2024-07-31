from fastapi import APIRouter
from shop.data_base import users, database
from shop.models import User, UserIn
from typing import List

router = APIRouter()


@router.get('/users', response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@router.post('/users', response_model=UserIn)
async def create_user(new_user: UserIn):
    query = users.insert().values(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password=new_user.password
    )
    await database.execute(query)
    return new_user


@router.put('/users/{user_id}', response_model=UserIn)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return new_user


@router.delete('/users/{user_id}', response_model=dict)
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'user deleted'}


@router.get("/fake_users/{count}", response_model=dict)
async def create_fake_users(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(first_name=f'first_name_{i}',
                                      last_name=f'last_name_{i}',
                                      email=f'{i}@mail.ru',
                                      password=f'{i}{i}{i}111',
                                      )
        await database.execute(query)

    return {'message': f'{count} fake users create'}
