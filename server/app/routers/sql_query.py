import re

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import ProgrammingError
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/sql_query")


@router.post("/")
def exec_query(
    query_struct: schemas.SQLQuery,
    db: Session = Depends(get_db),
    is_result: bool = True,
):
    db.execute(text("SET search_path TO public"))
    db_user = (
        db.query(models.UserDB)
        .filter(models.UserDB.login == query_struct.user)
        .first()
    )
    if not db_user:
        return {"error": "user not exist"}
    db.execute(text(f"SET search_path TO {query_struct.user}"))
    try:
        result = db.execute(text(query_struct.query))
        if query_struct.query.strip().lower().startswith("select"):
            explain_data = db.execute(
                text(
                    "EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON) "
                    + query_struct.query
                )
            ).scalar()
            print(explain_data)
            rows = result.mappings().all()
            return {
                "is_result": is_result,
                "name": explain_data[0]["Plan"].get(
                    "Relation Name", "Query Result"
                ),
                "headers": explain_data[0]["Plan"]["Output"],
                "data": [list(row.values()) for row in rows],
            }
        else:
            db.commit()
            table_name = extract_table_name(query_struct.query)
            return exec_query(
                schemas.SQLQuery(
                    query=f"select * from {table_name};",
                    user=query_struct.user,
                ),
                db,
                False,
            )
    except ProgrammingError as err:
        return str(err.orig)
    except UniqueViolation as err:
        return str(err)


def extract_table_name(query: str) -> str:
    query = re.sub(
        r"/\*.*?\*/|--.*?$", "", query, flags=re.DOTALL | re.MULTILINE
    )
    query = " ".join(query.split()).lower()

    patterns = {
        "create": r"create\s+(?:table|view)\s+(?:if\s+not\s+exists\s+)?([\w.]+)",
        "insert": r"insert\s+into\s+([\w.]+)",
        "update": r"update\s+([\w.]+)",
        "delete": r"delete\s+from\s+([\w.]+)",
        "alter": r"alter\s+table\s+([\w.]+)",
        "truncate": r"truncate\s+(?:table\s+)?([\w.]+)",
    }

    for cmd, pattern in patterns.items():
        if query.startswith(cmd):
            match = re.search(pattern, query)
            if match:
                return match.group(1)

    return None


def split_query(query: str) -> list[str]:
    query = query.strip().rstrip(";").replace("\n", " ")
    keywords = [
        "SELECT",
        "FROM",
        "JOIN",
        "WHERE",
        "GROUP BY",
        "ORDER BY",
        "HAVING",
        "LIMIT",
    ]
    for kw in keywords:
        query = re.sub(rf"\b{kw}\b", f"\n{kw}", query, flags=re.IGNORECASE)
    lines = [
        line.strip() for line in query.strip().split("\n") if line.strip()
    ]
    return lines


@router.post("/query_processing")
def query_processing(
    query_struct: schemas.SQLQuery, db: Session = Depends(get_db)
):
    tables_struct = {}
    subqueries = split_query(query_struct.query)
    print(subqueries)
    query = "SELECT * "
    db.execute(text(f"SET search_path TO {query_struct.user}"))
    for i in range(1, len(subqueries)):
        query += subqueries[i] + " "
        result = db.execute(text(query + ";"))
        explain_data = db.execute(
            text("EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON) " + query + ";")
        ).scalar()
        rows = result.mappings().all()
        tables_struct[subqueries[i]] = {
            "is_result": True,
            "name": "Query Result",
            "headers": explain_data[0]["Plan"]["Output"],
            "data": [list(row.values()) for row in rows],
        }
    query = query.replace("SELECT *", subqueries[0])
    result = db.execute(text(query + ";"))
    explain_data = db.execute(
        text("EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON) " + query + ";")
    ).scalar()
    rows = result.mappings().all()
    tables_struct[subqueries[i]] = {
        "is_result": True,
        "name": "Query Result",
        "headers": explain_data[0]["Plan"]["Output"],
        "data": [list(row.values()) for row in rows],
    }
    return tables_struct
