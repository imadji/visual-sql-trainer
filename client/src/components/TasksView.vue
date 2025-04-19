<template>
  <div class="tasks">
    <section class="tasks-panel">
      <div class="tasks-title">Задачи</div>
      <div class="tasks-items">
        <div v-for="(task, i) in tasks" :key="i" class="task-item" :class="{ active: i === activeTask }"
          @click="activeTask = i">
          <!-- <div v-if="task.completed" class="checkmark"></div> -->
          <img v-if="task.completed" class="checkmark" src="../assets/checkbox.png" alt="">
          <div class="task-title">{{ task.title }}</div>
          <div class="task-description">{{ task.short }}</div>
        </div>
      </div>
    </section>

    <section class="task-detail">
      <div class="tasks-title">Описание задачи</div>
      <div class="task-detail-container">
        <h2 class="task-detail-title">{{ tasks[activeTask].title }}</h2>
        <p class="task-detail-full">{{ tasks[activeTask].full }}</p>
      </div>
    </section>

    <section class="io-panel">
      <div class="tasks-title">Ввод/вывод</div>
      <div class="io-panel-container">
        <div class="console-output" ref="consoleOutput">
          <div v-for="(log, index) in consoleLogs" :key="index" class="log-message" :class="log.type">
            {{ log.message }}
            <button v-if="log.type === 'query'" class="debug-btn" @click="openDebugger(log.message)"
              title="Открыть в отладчике">
              <img src="../assets/info-helper.png" alt="">
            </button>
          </div>
        </div>
        <div class="editor-container">
          <!-- <textarea v-model="textRequest" placeholder="Введите SQL-запрос..."
          @keydown.enter.exact.prevent="sendRequest"></textarea> -->
          <textarea v-model="textRequest" placeholder="Введите SQL-запрос..." @keydown.enter.exact.prevent="sendRequest"
            @keydown.up.prevent="navigateHistory('up')" @keydown.down.prevent="navigateHistory('down')" />
        </div>
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
  display: flex;
  flex-direction: column;

  .tasks-title {
    flex-shrink: 0;
  }

  .tasks-items {
    flex: 1;
    overflow-y: auto;
    padding: 15px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;

    .task-item {
      width: 360px;
      min-height: 90px;
      border: 1px solid rgba(214, 214, 214, 0.1);
      border-radius: 15px;
      padding: 10px;
      cursor: pointer;
      position: relative;

      .checkmark {
        position: absolute;
        right: 5px;
        width: 25px;
      }

      .task-title {
        font-size: 18px;
      }

      .task-description {}
    }

    .task-item.active {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.task-detail {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  border-left: 1px solid rgba(255, 255, 255, 0.5);

  .task-detail-container {
    flex: 1;
    overflow-y: auto;
    margin: 15px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    background-color: rgba(214, 214, 214, 0.3);
    border-radius: 15px;

    .task-detail-title {
      font-size: 27px;
    }

    .task-detail-full {
      font-size: 20px;
    }
  }
}

.io-panel {
  width: 100%;
  display: flex;
  flex-direction: column;

  .io-panel-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex: 1;
    padding: 10px;
    gap: 10px;
  }

  .console-output {
    flex: 1;
    background-color: #1e1e1e;
    background-color: rgba(233, 241, 255, 1);
    border-radius: 6px;
    padding: 12px;
    font-family: "Consolas", monospace;
    font-size: 13px;
    overflow-y: auto;
    min-height: 0;
    scroll-behavior: smooth;

    .log-message {
      position: relative;
      margin-bottom: 8px;
      line-height: 1.4;
      white-space: pre-wrap;
      padding-right: 30px;

      &.info {
        color: #1f95cc;
      }

      &.error {
        color: #ad2727;
      }

      &.success {
        color: #23ad38;
      }

      &.query {
        color: #b0bec5;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 8px;
        color: #ffffff;
        background-color: rgba(0, 0, 0, 1);
        padding: 4px 8px;
        border-radius: 4px;
        font-family: "Consolas", monospace;
      }

      .debug-btn {
        position: absolute;
        right: 5px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        opacity: 0.5;
        transition: opacity 0.2s;
        padding: 0;

        &:hover {
          opacity: 1;
        }

        img {
          width: 16px;
          height: 16px;
          filter: invert(1);
        }
      }
    }
  }

  .editor-container {
    textarea {
      width: 100%;
      height: 120px;
      padding: 12px;
      border: 1px solid #3c3c3c;
      border-radius: 6px;
      font-family: "Consolas", monospace;
      font-size: 14px;
      resize: none;
      background-color: rgba(233, 241, 255, 1);
      color: #000;
      box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);

      &:focus {
        outline: none;
        border-color: #4a6fa5;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3), 0 0 0 2px rgba(74, 111, 165, 0.3);
      }

      &::placeholder {
        color: #5a5a5a;
      }
    }
  }

}
</style>
