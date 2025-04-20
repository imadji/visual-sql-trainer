"""
:mod:`gen_sql_task` -- Модуль для создания и проверки задач
===================================
.. moduleauthor:: ilya Barinov <i-barinov@it-serv.ru>
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Any, Literal
from openai import OpenAI
from sqlalchemy import text
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

TOGETHER_API_KEY = "460940d7b7b8c0bee5c1c7274afec77d2f4cea6f14c0f75c22108399a48fdf5a"

HINT_SYSTEM_PROMPT = (
    "Ты ассистент по обучению SQL. Не давай готовое решение. Вместо этого помоги ученику "
    "понять, в чём ошибка или что нужно использовать.\n"
    "Ты должен использовать только переданные таблицы. Укажи, какие SQL-конструкции "
    "или логика помогут продвинуться дальше, но не пиши SQL-запрос полностью."
)


client = OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1",
)

router = APIRouter(prefix="/gen-sql-task", tags=["SQL Task Generator"])


# region Pydantic
class SQLTable(BaseModel):
    """Модель таблиц пользователя"""

    is_result: bool
    name: str
    headers: List[str]
    data: List[List[Any]]


class TaskRequest(BaseModel):
    """Request на создание задания"""

    tables: List[SQLTable]
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class TaskResponse(BaseModel):
    """Response на создание задания"""

    task: str
    sql: str
    example_output: str


class CheckSQLRequest(BaseModel):
    user_sql: str
    expected_sql: str


class CheckSQLResponse(BaseModel):
    success: bool
    expected_result: List[dict[str, Any]]
    user_result: List[dict[str, Any]]
    message: str


class HintRequest(BaseModel):
    user_attempt: str
    tables: List[SQLTable]


class HintResponse(BaseModel):
    hint: str


# region Utils
def build_prompt_from_tables(tables: List[SQLTable]) -> str:
    """Функция создания промта для запроса к ИИ по данным таблиц

    :param tables: Таблицы пользователя
    """
    lines = ["У тебя есть следующие таблицы с данными:"]
    for table in tables:
        lines.append(f"\nТаблица `{table.name}`:")
        lines.append("Колонки: " + ", ".join(table.headers))
        lines.append("Примеры данных:")
        for row in table.data[:3]:
            lines.append(" - " + ", ".join(map(str, row)))
    return "\n".join(lines)


def generate_sql_task(tables: List[SQLTable], difficulty: str) -> dict:
    table_prompt = build_prompt_from_tables(tables)

    system_msg = (
        "Ты преподаватель SQL. Используй только те таблицы, что переданы ниже. "
        "Не придумывай дополнительные таблицы."
        f"Придумай SQL-задачу уровня сложности '{difficulty}' на русском языке.\n\n"
        "Включи в ответ:\n"
        "1. Подробное описание задачи с упоминанием нужных колонок\n"
        "2. SQL-запрос как решение задачи\n"
        "3. Пример результата в виде таблицы (markdown)\n\n"
        "Формат:\n"
        "ЗАДАЧА: <описание>\n"
        "SQL: <запрос>\n"
        "ПРИМЕР РЕЗУЛЬТАТА:\n"
        "| ... | ... |"
    )

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": table_prompt},
            ],
            temperature=0.7,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    if not response.choices[0].message.content:
        raise HTTPException(status_code=500, detail="LLM error")

    content = response.choices[0].message.content.strip()

    task = ""
    sql = ""
    output = ""

    if "ЗАДАЧА:" in content:
        parts = content.split("ЗАДАЧА:")[1].split("SQL:")
        task = parts[0].strip()
        rest = parts[1].strip() if len(parts) > 1 else ""

        if "ПРИМЕР РЕЗУЛЬТАТА:" in rest:
            sql, output = rest.split("ПРИМЕР РЕЗУЛЬТАТА:", 1)
            sql = sql.strip()
            output = output.strip()
        else:
            sql = rest.strip()

    return {"task": task, "sql": sql, "example_output": output}


def execute_sql(session: Session, query: str) -> List[dict[str, Any]]:
    """
    Выполняет SQL-запрос и возвращает результат в виде списка словарей.

    :param session: Активная SQLAlchemy-сессия
    :param query: SQL-запрос
    :return: Список строк как dict (ключи — имена колонок)
    """
    result = session.execute(text(query))
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result.fetchall()]


# region Routs


@router.post("/", response_model=TaskResponse)
def generate_task(request: TaskRequest):
    return generate_sql_task(request.tables, request.difficulty)


@router.post("/check", response_model=CheckSQLResponse)
def check_user_sql(
    data: CheckSQLRequest,
    session: Session = Depends(get_db),
):
    try:
        expected = execute_sql(session, data.expected_sql)
    except SQLAlchemyError as e:
        return CheckSQLResponse(
            success=False,
            expected_result=[],
            user_result=[],
            message=f"Ошибка в эталонном SQL: {str(e)}",
        )

    try:
        user = execute_sql(session, data.user_sql)
    except SQLAlchemyError as e:
        return CheckSQLResponse(
            success=False,
            expected_result=expected,
            user_result=[],
            message=f"Ошибка в SQL пользователя: {str(e)}",
        )

    success = sorted(expected, key=lambda x: sorted(x.items())) == sorted(
        user, key=lambda x: sorted(x.items())
    )

    return CheckSQLResponse(
        success=success,
        expected_result=expected,
        user_result=user,
        message="Результаты совпадают" if success else "Результаты не совпадают",
    )


@router.post("/hint", response_model=HintResponse)
def get_hint(data: HintRequest):
    """Помощ в выполнении заданий"""
    table_prompt = build_prompt_from_tables(data.tables)
    user_prompt = f"Попытка пользователя:\n{data.user_attempt}"

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "system", "content": HINT_SYSTEM_PROMPT},
                {"role": "user", "content": table_prompt + "\n\n" + user_prompt},
            ],
            temperature=0.8,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HINT LLM error: {str(e)}")

    content = response.choices[0].message.content.strip()
    return HintResponse(hint=content)
