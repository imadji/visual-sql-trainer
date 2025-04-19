from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal


class UserDB(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True)
    db_login = Column(String(50), unique=True)
    password = Column(String(128))
    db_password = Column(String(128))

    passed_tasks = relationship("PassedTasks", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(256), unique=True)
    solution = Column(String(528))

    users = relationship("PassedTasks", back_populates="task")


class PassedTasks(Base):
    __tablename__ = "passed_tasks"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("public.users.id"))
    task_id = Column(Integer, ForeignKey("public.tasks.id"))
    user_solution = Column(String(528))

    user = relationship("UserDB", back_populates="passed_tasks")
    task = relationship("Task", back_populates="users")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "tasks_schema"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "tasks_schema"}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("tasks_schema.categories.id"))

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "tasks_schema"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    registration_date = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "tasks_schema"}

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("tasks_schema.customers.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    status = Column(String(50), default="processing")

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"schema": "tasks_schema"}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("tasks_schema.orders.id"))
    product_id = Column(Integer, ForeignKey("tasks_schema.products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


def seed_database():
    with SessionLocal() as session:
        # 1. Заполнение категорий
        if not session.query(Category).first():
            categories = [
                Category(
                    name="Электроника",
                    description="Смартфоны, ноутбуки, планшеты и другие гаджеты",
                ),
                Category(
                    name="Одежда",
                    description="Мужская, женская и детская одежда",
                ),
                Category(
                    name="Книги",
                    description="Художественная и профессиональная литература",
                ),
                Category(
                    name="Продукты", description="Продукты питания и напитки"
                ),
                Category(
                    name="Спорт", description="Спортивные товары и инвентарь"
                ),
            ]
            session.add_all(categories)
            session.commit()

        # 2. Заполнение товаров
        if not session.query(Product).first():
            products = [
                Product(
                    name="iPhone 14",
                    description="Смартфон Apple",
                    price=999.99,
                    stock_quantity=50,
                    category=categories[0],
                ),
                Product(
                    name="Ноутбук ASUS ROG",
                    description="Игровой ноутбук",
                    price=1499.99,
                    stock_quantity=25,
                    category=categories[0],
                ),
                Product(
                    name="Джинсы Levi's",
                    description="Классические мужские джинсы",
                    price=89.99,
                    stock_quantity=100,
                    category=categories[1],
                ),
                Product(
                    name="Война и мир",
                    description="Роман Льва Толстого",
                    price=24.99,
                    stock_quantity=200,
                    category=categories[2],
                ),
                Product(
                    name="Оливковое масло",
                    description="Extra virgin, 1 литр",
                    price=12.99,
                    stock_quantity=150,
                    category=categories[3],
                ),
                Product(
                    name="Беговая дорожка",
                    description="Электрическая с 12 программами",
                    price=799.99,
                    stock_quantity=15,
                    category=categories[4],
                ),
                Product(
                    name="AirPods Pro",
                    description="Беспроводные наушники",
                    price=249.99,
                    stock_quantity=75,
                    category=categories[0],
                ),
                Product(
                    name="Кроссовки Nike",
                    description="Беговые кроссовки",
                    price=119.99,
                    stock_quantity=60,
                    category=categories[1],
                ),
                Product(
                    name="SQL для профессионалов",
                    description="Руководство по работе с базами данных",
                    price=39.99,
                    stock_quantity=45,
                    category=categories[2],
                ),
                Product(
                    name="Гантели 5 кг",
                    description="Резиновые гантели",
                    price=29.99,
                    stock_quantity=80,
                    category=categories[4],
                ),
            ]
            session.add_all(products)
            session.commit()

        # 3. Заполнение клиентов
        if not session.query(Customer).first():
            customers = [
                Customer(
                    name="Иван Петров",
                    email="ivan@example.com",
                    phone="+79161234567",
                    registration_date=datetime(2023, 1, 15),
                ),
                Customer(
                    name="Елена Смирнова",
                    email="elena@example.com",
                    phone="+79167654321",
                    registration_date=datetime(2023, 2, 20),
                ),
                Customer(
                    name="Алексей Иванов",
                    email="alex@example.com",
                    phone="+79165557788",
                    registration_date=datetime(2023, 3, 10),
                ),
                Customer(
                    name="Мария Сидорова",
                    email="maria@example.com",
                    phone="+79169991122",
                    registration_date=datetime(2023, 4, 5),
                ),
                Customer(
                    name="Дмитрий Кузнецов",
                    email="dmitry@example.com",
                    phone="+79163334455",
                    registration_date=datetime(2023, 5, 12),
                ),
            ]
            session.add_all(customers)
            session.commit()

        # 4. Заполнение заказов
        if not session.query(Order).first():
            orders = [
                Order(
                    customer=customers[0],
                    order_date=datetime(2023, 6, 1, 10, 15),
                    status="completed",
                ),
                Order(
                    customer=customers[1],
                    order_date=datetime(2023, 6, 2, 14, 30),
                    status="completed",
                ),
                Order(
                    customer=customers[2],
                    order_date=datetime(2023, 6, 3, 11, 45),
                    status="processing",
                ),
                Order(
                    customer=customers[3],
                    order_date=datetime(2023, 6, 4, 16, 20),
                    status="shipped",
                ),
                Order(
                    customer=customers[0],
                    order_date=datetime(2023, 6, 5, 9, 10),
                    status="completed",
                ),
                Order(
                    customer=customers[4],
                    order_date=datetime(2023, 6, 6, 13, 25),
                    status="processing",
                ),
                Order(
                    customer=customers[1],
                    order_date=datetime(2023, 6, 7, 15, 50),
                    status="new",
                ),
            ]
            session.add_all(orders)
            session.commit()

        # 5. Заполнение позиций заказов
        if not session.query(OrderItem).first():
            order_items = [
                OrderItem(
                    order=orders[0],
                    product=products[0],
                    quantity=1,
                    unit_price=999.99,
                ),
                OrderItem(
                    order=orders[0],
                    product=products[6],
                    quantity=1,
                    unit_price=49.99,
                ),
                OrderItem(
                    order=orders[1],
                    product=products[2],
                    quantity=1,
                    unit_price=89.99,
                ),
                OrderItem(
                    order=orders[1],
                    product=products[7],
                    quantity=1,
                    unit_price=119.99,
                ),
                OrderItem(
                    order=orders[2],
                    product=products[5],
                    quantity=1,
                    unit_price=799.99,
                ),
                OrderItem(
                    order=orders[3],
                    product=products[3],
                    quantity=2,
                    unit_price=24.99,
                ),
                OrderItem(
                    order=orders[3],
                    product=products[4],
                    quantity=1,
                    unit_price=12.99,
                ),
                OrderItem(
                    order=orders[3],
                    product=products[8],
                    quantity=1,
                    unit_price=39.99,
                ),
                OrderItem(
                    order=orders[4],
                    product=products[8],
                    quantity=1,
                    unit_price=39.99,
                ),
                OrderItem(
                    order=orders[5],
                    product=products[1],
                    quantity=1,
                    unit_price=1499.99,
                ),
                OrderItem(
                    order=orders[5],
                    product=products[9],
                    quantity=2,
                    unit_price=29.99,
                ),
                OrderItem(
                    order=orders[6],
                    product=products[7],
                    quantity=1,
                    unit_price=119.99,
                ),
            ]
            session.add_all(order_items)
            session.commit()

            # 6. Обновление общей суммы заказов
            for order in orders:
                order.total_amount = sum(
                    item.quantity * item.unit_price for item in order.items
                )
            session.commit()

        if not session.query(Task).first():
            tasks = [
                Task(
                    title="Анализ продаж по категориям",
                    description="Написать запрос, который выводит суммарные продажи по каждой категории товаров за последний месяц",
                    solution="""SELECT c.name, SUM(oi.quantity * oi.unit_price) 
                            FROM order_items oi
                            JOIN products p ON oi.product_id = p.id
                            JOIN categories c ON p.category_id = c.id
                            JOIN orders o ON oi.order_id = o.id
                            WHERE o.order_date >= NOW() - INTERVAL '1 month'
                            GROUP BY c.name""",
                ),
                Task(
                    title="Поиск VIP-клиентов",
                    description="Найти клиентов, совершивших заказы на сумму более 10000 руб за последние 3 месяца",
                    solution="""SELECT c.name, SUM(o.total_amount) as total_spent
                            FROM customers c
                            JOIN orders o ON c.id = o.customer_id
                            WHERE o.order_date >= NOW() - INTERVAL '3 months'
                            GROUP BY c.id
                            HAVING SUM(o.total_amount) > 10000""",
                ),
                Task(
                    title="Товары с низким остатком",
                    description="Вывести товары, количество которых на складе меньше 10, с указанием категории",
                    solution="""SELECT p.name, c.name as category, p.stock_quantity
                            FROM products p
                            JOIN categories c ON p.category_id = c.id
                            WHERE p.stock_quantity < 10
                            ORDER BY p.stock_quantity ASC""",
                ),
                Task(
                    title="Средний чек по месяцам",
                    description="Рассчитать средний чек заказов по месяцам за последний год",
                    solution="""SELECT 
                                DATE_TRUNC('month', order_date) as month,
                                AVG(total_amount) as avg_order_value
                            FROM orders
                            WHERE order_date >= NOW() - INTERVAL '1 year'
                            GROUP BY DATE_TRUNC('month', order_date)
                            ORDER BY month""",
                ),
                Task(
                    title="Анализ повторных покупок",
                    description="Найти товары, которые чаще всего покупают повторно (которые есть минимум в 2 разных заказах)",
                    solution="""SELECT p.name, COUNT(DISTINCT oi.order_id) as order_count
                            FROM products p
                            JOIN order_items oi ON p.id = oi.product_id
                            GROUP BY p.id
                            HAVING COUNT(DISTINCT oi.order_id) >= 2
                            ORDER BY order_count DESC""",
                ),
            ]

            session.add_all(tasks)
            session.commit()
