from typing import Union
import sqlite3

from tasklist.models.task import Task
from tasklist.models.newtask import NewTask
from tasklist.models.updatetask import UpdateTask


def add_task(new_task: NewTask):
    with sqlite3.connect("tasks.sqlite3") as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO tasks (
                title,
                description,
                priority,
                due_date
            ) VALUES (:title, :description, :priority, :due_date)
        """, new_task.__dict__)

        task = Task(
            id=cur.lastrowid,
            title=new_task.title,
            description=new_task.description,
            priority=new_task.priority,
            due_date=new_task.due_date
        )

        con.commit()
    return task


def get_tasks(completed: Union[bool, None] = None, priority: Union[int, None] = None):
    with sqlite3.connect("tasks.sqlite3") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute("""
            SELECT
                id,
                title,
                description,
                priority,
                due_date,
                completed
            FROM
                tasks
            WHERE
                (:completed IS NULL OR completed=:completed) AND
                (:priority IS NULL OR priority=:priority)
        """, { "completed": completed, "priority": priority})

        return [Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            due_date=row["due_date"],
            completed=row["completed"]
        ) for row in result.fetchall()]


def get_task(task_id: int):
    with sqlite3.connect("tasks.sqlite3") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute("""
            SELECT
                id,
                title,
                description,
                priority,
                due_date,
                completed
            FROM
                tasks
            WHERE
                id=?
        """, [task_id])

        row = result.fetchone()
        if row is None:
            return None
        
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            due_date=row["due_date"],
            completed=row["completed"]
        )

def delete_task(task_id: int):
    with sqlite3.connect("tasks.sqlite3") as con:
        cur = con.cursor()
        result = cur.execute("""
            DELETE FROM
                tasks
            WHERE
                id=?
        """, [task_id])


def update_task(task_id: int, update_task: UpdateTask):
    with sqlite3.connect("tasks.sqlite3") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute("""
            UPDATE tasks
            SET
                title=COALESCE(:title, title),
                description=COALESCE(:description, description),
                priority=COALESCE(:priority, priority),
                due_date=COALESCE(:due_date, due_date),
                completed=COALESCE(:completed, completed)
            WHERE
                id=:task_id
            RETURNING *
        """, {
            "task_id": task_id,
            "title": update_task.title,
            "description": update_task.description,
            "priority": update_task.priority,
            "due_date": update_task.due_date,
            "completed": update_task.completed
        })

        row = result.fetchone()
        if row is None:
            return None
        
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            due_date=row["due_date"],
            completed=row["completed"]
        )
