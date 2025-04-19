<template>
  <div class="workspace">
    <div class="switcher">
      <!-- тут иконка которая использует метод goHome -->
      <!-- если svg то вынести svg файл отдельно в assets -->
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
import { useRouter } from "vue-router";

const router = useRouter();
const currentView = ref("sandbox");

const goHome = async () => {
  router.push("/");
};
</script>

<style lang="scss" scoped></style>
