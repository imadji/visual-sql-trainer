<template>
  <div class="tasks">
    <section class="tasks-panel">
      <div class="tasks-title">Задачи</div>
      <div class="tasks-items">
        <div v-for="(task, i) in tasks" :key="i" class="task-item" :class="{ active: i === activeTask }"
          @click="activeTask = i">
          <div class="task-title">{{ task.title }}</div>
          <div class="task-description">{{ task.short }}</div>
          <div v-if="task.completed" class="checkmark">✓</div>
        </div>
      </div>
    </section>

    <section class="task-detail">
      <div class="tasks-title">Описание задачи</div>
      <h2 class="task-title">{{ tasks[activeTask].title }}</h2>
      <p class="task-full">{{ tasks[activeTask].full }}</p>
    </section>

    <section class="io-panel">
      <div class="tasks-title">Ввод/вывод</div>
      <div class="editor">
        <textarea v-model="query" placeholder="SELECT ..."></textarea>
        <button class="run-btn" @click="runQuery">▶</button>
      </div>
      <div class="output">
        <pre>{{ result }}</pre>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";

const tasks = ref([
  {
    title: "Простое извлечение данных",
    short: "Выведите имена всех клиентов...",
    full: "Выведите имена всех клиентов из таблицы customers, проживающих в городе 'Москва'.",
    completed: true,
    mockResult: [
      { name: "Иван Петров" },
      { name: "Мария Смирнова" },
    ],
  },
  {
    title: "Агрегация и группировка",
    short: "Найдите количество заказов...",
    full: "Найдите количество заказов, сделанных каждым клиентом.",
    completed: false,
    mockResult: [
      { customer_name: "Иван Петров", orders_count: 3 },
      { customer_name: "Анна Иванова", orders_count: 5 },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
  {
    title: "Объединение таблиц (JOIN)",
    short: "Выведите список заказов...",
    full: `Выведите список заказов с именем клиента и названием товара. Используйте таблицы orders, customers, products.`,
    completed: false,
    mockResult: [
      { order_id: 1, customer_name: "Иван Петров", product_name: "Ноутбук" },
      { order_id: 2, customer_name: "Анна Иванова", product_name: "Телефон" },
    ],
  },
]);

const activeTask = ref(0);
const query = ref(tasks.value[activeTask.value].full);
const result = ref([]);

function selectTask(index) {
  activeTask.value = index;
  query.value = tasks.value[index].full;
  result.value = [];
}

function runQuery() {
  result.value = tasks.value[activeTask.value].mockResult || [];
}
</script>

<style lang="scss" scoped>
.tasks {
  width: 100%;
  height: 80vh;
  display: flex;
  flex-direction: row;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 15px;
}

.tasks-title {
  width: 100%;
  font-size: 35px;
  font-weight: 900;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  padding: 10px;
}

.tasks-panel {
  height: 100%;
  min-width: 400px;

  .tasks-items {
    height: 100%;
    overflow: scroll;
    padding: 15px 0;
    width: 100%;
    // display: flex;
    // flex-direction: column;
    // align-items: center;
    // justify-content: center;
    // gap: 20px;

    .task-item{
      width: 360px;
      height: 90px;
      border: 1px solid rgba(214, 214, 214, 0.1);
      border-radius: 15px;
    }
  }
}

.task-detail {
  width: 100%;
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  // background-color: rgb(88, 92, 96);
}

.io-panel {
  width: 100%;
  // background-color: rgb(88, 92, 96);
}
</style>
