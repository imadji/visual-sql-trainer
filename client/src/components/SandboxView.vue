<template>
  <div class="sandbox">
    <h2>Песочница</h2>
    <div class="status">Статус: Готов к работе</div>
    <div class="editor">
      <textarea placeholder="Введите запрос..."></textarea>
    </div>
    <button @click="executeQuery">Выполнить</button>
    <div class="results">
      <h3>Результаты:</h3>
      <pre>{{ queryResults }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const queryResults = ref("");

const executeQuery = () => {
  queryResults.value = "rezultat";
};
</script>

<style lang="scss" scoped></style>
