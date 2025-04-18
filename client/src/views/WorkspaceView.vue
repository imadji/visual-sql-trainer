<template>
  <div>
    <StatusSwitcher />
    <div v-if="currentView === 'tasks'">
      <h2>Задания</h2>
      <p>Дебаг таблицы</p>
    </div>
    <div v-else>
      <h2>Песочница</h2>
      <p>Статус: ...</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import StatusSwitcher from "@/components/StatusSwitcher.vue";

const currentView = ref("tasks");
</script>
