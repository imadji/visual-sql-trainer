<template>
  <div class="container">
    <HomeHeader @open-auth="showAuthModal" />
    <HomeMain />
    <hr />
    <div class="train-container">
      <div class="train-text">
        <label>Тренируй свои навыки</label>
        <span
          >SQL — это навык, который лучше всего развивается в практике. Внутри тебя ждут
          интерактивные задания, живые примеры и понятные объяснения. От простых SELECT до сложных
          JOIN и подзапросов — ты сам решаешь темп и направление. Попробуй — и поймешь, что учиться
          можно интересно.
        </span>
      </div>
    </div>
    <AuthModal v-if="isModalVisible" :mode="modalMode" @close="hideAuthModal" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import AuthModal from "@/components/AuthModal.vue";
import HomeHeader from "./HomeHeader.vue";
import HomeMain from "./HomeMain.vue";

const isModalVisible = ref(false);
const modalMode = ref("login");

const showAuthModal = (mode) => {
  modalMode.value = mode;
  isModalVisible.value = true;
};

const hideAuthModal = () => {
  isModalVisible.value = false;
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  padding-left: 2%;
  padding-right: 2%;
  padding-top: 20px;
}

hr {
  height: 2px;
  border: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
}

.train-container {
  margin-top: 50px;
  height: 250px;

  .train-text {
    display: flex;
    flex-direction: column;
    label {
      font-size: 42px;
    }
    span {
      font-size: 20px;
    }
  }
}
</style>
