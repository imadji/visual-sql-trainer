<template>
  <div class="tasks">
    <h2>Задания</h2>
    <div class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task">
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <pre>{{ task.sqlExample }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const tasks = ref([
  {
    id: 1,
    title: "test data",
    description: "Напишите SQL-запрос",
    sqlExample: "SELECT name FROM employees;",
  },
  {
    id: 2,
    title: "test data",
    description: "Напишите SQL-запрос",
    sqlExample: 'SELECT name, salary FROM employees WHERE department = "IT";',
  },
]);
</script>

<style lang="scss" scoped></style>
