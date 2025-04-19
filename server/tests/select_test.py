import requests
import json

api_url = "http://localhost:8000/"
headers = {"accept": "application/json", "Content-Type": "application/json"}


def reg():
    requests.post(
        api_url + "auth/reg",
        json={"login": "test", "password": "test"},
        headers=headers,
    )


def create_table():
    r = requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ); """,
        },
        headers=headers,
    )


def fill_table():
    requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """INSERT INTO users (username, email) 
            VALUES ('ivan_ivanov', 'ivan@example.com'); """,
        },
        headers=headers,
    )
    print(1)
    requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """INSERT INTO users (username, email) 
            VALUES ('qwe_qwe', 'qwe@example.com'); """,
        },
        headers=headers,
    )
    print(1)
    requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """INSERT INTO users (username, email) 
            VALUES ('zxc', 'zxc@example.com'); """,
        },
        headers=headers,
    )
    print(1)


def select_table():
    response = requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """SELECT * FROM users;""",
        },
        headers=headers,
    )
    print(response.content)


if __name__ == "__main__":
    reg()
    create_table()
    fill_table()
    select_table()
