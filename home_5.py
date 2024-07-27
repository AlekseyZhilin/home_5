from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


tasks = []


class Task(BaseModel):
    id: int
    head: str
    description: str
    status: Optional[bool] = None


class TaskIn(BaseModel):
    head: str
    description: str
    status: Optional[bool] = None


@app.get('/tasks/', response_model=list[Task])
async def show_tasks():
    return tasks


@app.get('/tasks/{id}', response_model=dict)
async def show_task(id: int):
    for i in range(len(tasks)):
        if tasks[i].id == id:
            return {'task': f'задание найдено {tasks[i]}'}
    return {'message': f'задание с id {id} не найдено'}


@app.post("/tasks/", response_model=list[Task])
async def create_task(new_task: TaskIn):
    tasks.append(
        Task(
            id=len(tasks) + 1,
            head=new_task.head, description=new_task.description, status=new_task.status
        )
    )
    return tasks


@app.put("/tasks/{id}", response_model=Task)
async def update_task(id: int, edit_task: TaskIn):
    find_task = None
    for i in range(len(tasks)):
        if tasks[i].id == id:
            find_task = tasks[i]
            break

    if find_task:
        find_task.head = edit_task.head
        find_task.description = edit_task.description
        find_task.status = edit_task.status

        return find_task

    raise HTTPException(status_code=404, detail='task no found')


@app.delete("/tasks/{id}", response_model=dict)
async def delete_task(id: int):
    for i in range(len(tasks)):
        if tasks[i].id == id:
            tasks.remove(tasks[i])
            return {'message': f'задача с id {id} удалена'}

    raise HTTPException(status_code=404, detail='task no found')

