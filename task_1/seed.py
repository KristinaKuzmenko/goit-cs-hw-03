import logging
from random import randint

from faker import Faker
from psycopg2 import DatabaseError

from connect_pg import connect


fake = Faker("en_US")
NUMBER_OF_USERS = 100
NUMBER_OF_TASKS = 500


def insert_data_in_users(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        for _ in range(NUMBER_OF_USERS):
            name = fake.name()
            email = fake.email()
            cursor.execute(sql_stmt, (name, email))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()


def insert_in_status(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        statuses = ["new", "in_progress", "completed"]
        for status in statuses:
            cursor.execute(sql_stmt, (status,))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()


def insert_data_in_tasks(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        for _ in range(NUMBER_OF_TASKS):
            title = fake.word()
            description = fake.sentence()
            status_id = randint(1, 3)
            user_id = randint(1, NUMBER_OF_USERS)
            cursor.execute(sql_stmt, (title, description, status_id, user_id))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    stmt_users = """
    INSERT INTO users (fullname, email) VALUES (%s, %s);
    """

    stmt_status = """
    INSERT INTO status (name) VALUES (%s);
    """

    stmt_tasks = """
    INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
    """

    try:
        with connect() as conn:
            insert_data_in_users(conn, stmt_users)
            insert_in_status(conn, stmt_status)
            insert_data_in_tasks(conn, stmt_tasks)
    except RuntimeError as e:
        logging.error(e)
