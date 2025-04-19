import requests

api_url = "http://localhost:8000/"
headers = {"accept": "application/json", "Content-Type": "application/json"}
user = "test"


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
            "user": user,
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
            "user": user,
            "query": """INSERT INTO users (username, email) 
            VALUES ('ivan_ivanov', 'ivan@example.com'); """,
        },
        headers=headers,
    )
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """INSERT INTO users (username, email) 
            VALUES ('qwe_qwe', 'qwe@example.com'); """,
        },
        headers=headers,
    )
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """INSERT INTO users (username, email) 
            VALUES ('zxc', 'zxc@example.com'); """,
        },
        headers=headers,
    )


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


[
    {
        "Plan": {
            "Node Type": "Hash Join",
            "Parallel Aware": False,
            "Async Capable": False,
            "Join Type": "Inner",
            "Startup Cost": 12.76,
            "Total Cost": 26.64,
            "Plan Rows": 1,
            "Plan Width": 356,
            "Actual Startup Time": 0.016,
            "Actual Total Time": 0.021,
            "Actual Rows": 6,
            "Actual Loops": 1,
            "Output": ["u.name", "o.product_name", "o.price", "o.order_date"],
            "Inner Unique": True,
            "Hash Cond": "(o.user_id = u.id)",
            "Plans": [
                {
                    "Node Type": "Seq Scan",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Relation Name": "orders",
                    "Schema": "joiner",
                    "Alias": "o",
                    "Startup Cost": 0.0,
                    "Total Cost": 13.62,
                    "Plan Rows": 97,
                    "Plan Width": 242,
                    "Actual Startup Time": 0.003,
                    "Actual Total Time": 0.006,
                    "Actual Rows": 18,
                    "Actual Loops": 1,
                    "Output": [
                        "o.id",
                        "o.user_id",
                        "o.product_name",
                        "o.price",
                        "o.order_date",
                    ],
                    "Filter": "(o.price > '50'::numeric)",
                    "Rows Removed by Filter": 12,
                },
                {
                    "Node Type": "Hash",
                    "Parent Relationship": "Inner",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Startup Cost": 12.75,
                    "Total Cost": 12.75,
                    "Plan Rows": 1,
                    "Plan Width": 122,
                    "Actual Startup Time": 0.008,
                    "Actual Total Time": 0.008,
                    "Actual Rows": 3,
                    "Actual Loops": 1,
                    "Output": ["u.name", "u.id"],
                    "Hash Buckets": 1024,
                    "Original Hash Buckets": 1024,
                    "Hash Batches": 1,
                    "Original Hash Batches": 1,
                    "Peak Memory Usage": 9,
                    "Plans": [
                        {
                            "Node Type": "Seq Scan",
                            "Parent Relationship": "Outer",
                            "Parallel Aware": False,
                            "Async Capable": False,
                            "Relation Name": "users",
                            "Schema": "joiner",
                            "Alias": "u",
                            "Startup Cost": 0.0,
                            "Total Cost": 12.75,
                            "Plan Rows": 1,
                            "Plan Width": 122,
                            "Actual Startup Time": 0.002,
                            "Actual Total Time": 0.003,
                            "Actual Rows": 3,
                            "Actual Loops": 1,
                            "Output": ["u.name", "u.id"],
                            "Filter": "((u.name)::text = 'Иван Иванов'::text)",
                            "Rows Removed by Filter": 6,
                        }
                    ],
                },
            ],
        },
        "Planning Time": 0.05,
        "Triggers": [],
        "Execution Time": 0.029,
    }
]
