<template>
  <div class="container">
    <header class="header-container">
      <span>
        
        <img src="../assets/Logo-mini.png" alt="">
      </span>
      <button class="sign-up-btn" @click="showAuthModal('login')">Вход</button>
      <!-- <button @click="showAuthModal('register')">Регистрация</button> -->
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

<style  lang="scss" scoped>
.container{
  height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
}

.header-container{
width: 100%;
display: flex;
justify-content: space-between;
  button{
    background-color: var(--shadow-background);
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 20px;
    padding-right: 20px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
</style>
