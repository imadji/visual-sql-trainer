<template>
  <div class="container">
    <header>
      <button @click="showAuthModal('login')">Вход</button>
      <button @click="showAuthModal('register')">Регистрация</button>
    </header>
    <main>
      <h1>Добро пожаловать в SQL Trainer</h1>
      <p>Практикуйте SQL в интерактивной среде</p>
    </main>
    <AuthModal v-if="isModalVisible" :mode="modalMode" @close="hideAuthModal" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import AuthModal from "@/components/AuthModal.vue";

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

<style scoped>
.container{
  background-color: var(--background-color);
  color: var(--text-color);
}
</style>
