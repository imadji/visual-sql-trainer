import requests

api_url = "http://localhost:8000/"
headers = {"accept": "application/json", "Content-Type": "application/json"}
user = "joiner"


def reg():
    requests.post(
        api_url + "auth/reg",
        json={"login": user, "password": "test"},
        headers=headers,
    )


def create_table():
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );""",
        },
        headers=headers,
    )
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                product_name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                order_date DATE NOT NULL DEFAULT CURRENT_DATE
            );""",
        },
        headers=headers,
    )


def fill_table():
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """INSERT INTO users (name, email) VALUES 
            ('Иван Иванов', 'qwe@qqwe.com'),
            ('Петр Петров', '123@qqwe.com'),
            ('Мария Сидорова', 'asd@qqwe.com');""",
        },
        headers=headers,
    )
    requests.post(
        api_url + "sql_query",
        json={
            "user": user,
            "query": """INSERT INTO orders (user_id, product_name, price) VALUES
            (1, 'Ноутбук', 999.99),
            (1, 'Мышь', 49.99),
            (2, 'Клавиатура', 79.99),
            (3, 'Монитор', 199.99),
            (3, 'Коврик для мыши', 9.99);
            """,
        },
        headers=headers,
    )


def select_table():
    response = requests.post(
        api_url + "sql_query",
        json={
            "user": "test",
            "query": """SELECT u.name, o.product_name, o.price, o.order_date
            FROM users u
            JOIN orders o ON u.id = o.user_id
            WHERE u.name = 'Иван Иванов' AND o.price > 50;
            """,
        },
        headers=headers,
    )
    print(response.content)


if __name__ == "__main__":
    reg()
    create_table()
    fill_table()
    select_table()
