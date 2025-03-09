from typing import List, Union
from fastapi import FastAPI, HTTPException
from tasklist import db
from tasklist.models.task import Task 
from tasklist.models.newtask import NewTask
from tasklist.models.updatetask import UpdateTask


app = FastAPI()


@app.post("/tasks")
def add_task(new_task: NewTask) -> Task:
    task = db.add_task(new_task)
    return task


@app.get("/tasks")
def get_tasks(completed: Union[bool, None] = None, priority: Union[int, None] = None) -> List[Task]:
    return db.get_tasks(completed, priority)


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    task = db.get_task(task_id)
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task
    

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_task: UpdateTask) -> Task:
    task = db.update_task(task_id, update_task)
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db.delete_task(task_id)
    return { "message": "Task deleted successfully." }
