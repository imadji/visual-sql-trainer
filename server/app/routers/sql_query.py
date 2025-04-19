from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/sql_query")


@router.post("/")
def read_item(query_struct: schemas.SQLQuery, db: Session = Depends(get_db)):
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
        table_name = getattr(
            result.cursor.description[0], "table_name", "query_result"
        )
        if query_struct.query.strip().lower().startswith("select"):
            rows = result.mappings().all()
            return refactor_table_struct(rows, table_name)
        else:
            db.commit()
            return {"status": "success", "rowcount": result.rowcount}
    except ProgrammingError as err:
        return str(err.orig)


def refactor_table_struct(table_struct, table_name):
    return {
        "name": table_name,
        "headers": list(table_struct[0].keys()) if table_struct else [],
        "data": [list(row.values()) for row in table_struct],
    }
