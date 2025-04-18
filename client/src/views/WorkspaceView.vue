<template>
  <div class="workspace">
    <div class="switcher">
      <button @click="currentView = 'tasks'" :class="{ active: currentView === 'tasks' }">
        Задания
      </button>
      <button @click="currentView = 'sandbox'" :class="{ active: currentView === 'sandbox' }">
        Песочница
      </button>
    </div>

    <TasksView v-if="currentView === 'tasks'" />
    <SandboxView v-else />
  </div>
</template>

<script setup>
import { ref } from "vue";
import TasksView from "@/components/TasksView.vue";
import SandboxView from "@/components/SandboxView.vue";

const currentView = ref("tasks");
</script>

<style lang="scss" scoped></style>
