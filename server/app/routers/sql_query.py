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
def exec_query(query_struct: schemas.SQLQuery, db: Session = Depends(get_db)):
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
