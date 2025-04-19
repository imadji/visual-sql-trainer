from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.routers.sql_query import exec_query
from app import models, schemas
from ..database import get_db

router = APIRouter(prefix="/sql_task")


@router.get("/get_tasks")
def get_task(user_login: str, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.UserDB)
        .filter(models.UserDB.login == user_login)
        .first()
    )
    if db_user:
        tasks = db.query(models.Task).all()
        structured_tasks = []
        for task in tasks:
            user_solution = find_user_solution(db_user, task)
            structured_tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "user_solution": user_solution,
                    "solved": user_solution != "",
                }
            )
        return {"tasks": structured_tasks}

    return {"tasks": []}


@router.post("/solve_task")
def solve_task(solution: schemas.TaskSoltion, db: Session = Depends(get_db)):
    db.execute(text("SET search_path TO public"))
    task = (
        db.query(models.Task)
        .filter(models.Task.id == solution.task_id)
        .first()
    )

    db.execute(text("SET search_path TO tasks_schema"))
    result = exec_query(
        schemas.SQLQuery(query=solution.query, user="tasks_schema"), db=db
    )
    real_result = exec_query(
        schemas.SQLQuery(query=task.solution, user="tasks_schema"), db=db
    )
    if result == real_result:
        db.execute(text("SET search_path TO public"))
        db_user = (
            db.query(models.UserDB)
            .filter(models.UserDB.login == solution.user)
            .first()
        )
        db.execute(text("SET search_path TO public"))
        passed_task = models.PassedTasks(
            user_id=db_user.id, task_id=task.id, user_solution=solution.query
        )
        db.add(passed_task)
        db.commit()
        db.refresh(passed_task)
        return {"status": True, "result": result}
    return {"status": False, "result": result}


def find_user_solution(user: models.UserDB, task: models.Task) -> str:
    for passed_task in user.passed_tasks:
        if passed_task.task_id == task.id:
            return passed_task.user_solution
    return ""
