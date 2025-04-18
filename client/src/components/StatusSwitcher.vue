<template>
  <div class="switcher">
    <button @click="switchView('tasks')" :class="{ active: currentView === 'tasks' }">
      Задания
    </button>
    <button @click="switchView('sandbox')" :class="{ active: currentView === 'sandbox' }">
      Песочница
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const currentView = ref("tasks");

const switchView = (view) => {
  currentView.value = view;
};
</script>
