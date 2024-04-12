import logging
from psycopg2 import DatabaseError

from connect_pg import connect


def create_table(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        cursor.execute(sql_stmt)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with open("create_tables.sql", "r", encoding="utf-8") as f:
        stmt = f.read()

    try:
        with connect() as conn:
            create_table(conn, stmt)
    except RuntimeError as e:
        logging.error(e)
