<template>
  <div class="workspace">
    <header>
      <span @click="goHome">
        <img src="../assets/Logo-mini.png" alt="" />
        <label>SQL Coding</label>
      </span>
      <div class="toggle-switch">
        <div
          class="switch-option"
          :class="{ active: currentView === 'tasks' }"
          @click="currentView = 'tasks'"
        >
          Задания
        </div>
        <div
          class="switch-option"
          :class="{ active: currentView === 'sandbox' }"
          @click="currentView = 'sandbox'"
        >
          Песочница
        </div>
        <div class="switch-indicator" :class="currentView" />
      </div>
    </header>

    <TasksView v-if="isVisibleTask" :isVisible="isVisibleTask" />
    <SandboxView v-else />
    <HomeFooter />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import TasksView from "@/components/TasksView.vue";
import SandboxView from "@/components/SandboxView.vue";
import { useRouter } from "vue-router";
import HomeFooter from "./HomeView/HomeFooter.vue";
import { gsap } from "gsap";

onMounted(() => {
  gsap.from("span", { duration: 1, y: -50, opacity: 0, ease: "power2.out" });
});

const router = useRouter();
const currentView = ref("sandbox");

const goHome = async () => {
  router.push("/");
};

const isVisibleTask = computed(() => {
  if (currentView.value === "tasks") return true;
});
</script>

<style lang="scss" scoped>
.workspace {
  height: 100vh;
  background-color: var(--background-color);
  padding: 0 1%;
  color: var(--text-color);
  font-family: "Ubuntu", sans-serif;

  header {
    width: 100%;
    height: 10vh;
    display: grid;
    grid-template-columns: repeat(2, 40%);
    align-items: center;

    span {
      display: flex;
      align-items: center;

      label {
        color: var(--text-color);
        font-size: 26px;
        font-weight: 500;
        transform: translateX(-10px);
      }
    }

    .toggle-switch {
      position: relative;
      display: flex;
      width: 220px;
      background-color: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 999px;
      overflow: hidden;
      height: 40px;
      margin-left: 20px;
    }

    .switch-option {
      flex: 1;
      text-align: center;
      line-height: 40px;
      z-index: 2;
      cursor: pointer;
      font-weight: 500;
      color: var(--text-color);
      transition: color 0.3s ease;
    }

    .switch-option.active {
      color: #fff;
      font-weight: 600;
    }

    .switch-indicator {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 50%;
      background: var(--shadow-background);
      border-radius: 999px;
      transition: transform 0.3s ease;
      z-index: 1;
    }

    .switch-indicator.tasks {
      transform: translateX(0%);
    }

    .switch-indicator.sandbox {
      transform: translateX(100%);
    }
  }
}
</style>
