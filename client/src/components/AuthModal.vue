<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <!-- добавить икноку закрытия -->
      <button class="close-btn" @click="close">Х</button>
      <h2>{{ mode === "login" ? "Вход" : "Регистрация" }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="login">Логин</label>
          <input id="login" v-model="login" type="text" placeholder="Введите ваш логин" required />
        </div>

        <div class="form-group">
          <label for="password">Пароль</label>
          <input id="password" v-model="password" type="password" placeholder="Введите пароль" required />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="submit-btn">
          {{ mode === "login" ? "Войти" : "Зарегистрироваться" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
interface TableData {
  name: string;
  headers: string[];
  data: any[][];
}

import { ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const props = defineProps<{
  mode: "login" | "register";
}>();

const emit = defineEmits(["close"]);

const login = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const close = () => {
  emit("close");
};

const handleSubmit = async () => {
  errorMessage.value = "";
  isLoading.value = true;

  try {
    const credentials = {
      login: login.value,
      password: password.value,
    };
    let response;
    if (props.mode === "login") {
      response = await authStore.login(credentials);
    } else {
      response = await authStore.register(credentials);
    }

    const tables = response?.tables || [];
    if (response?.status) {
      const tablesData = tables.map((table: TableData) => ({
        name: table.name,
        headers: table.headers,
        data: table.data,
        position: {
          x: Math.floor(Math.random() * 100),
          y: Math.floor(Math.random() * 100),
        },
        width: 500,
        isDragging: false,
      }));
      authStore.setTables(tablesData);
      close();
      router.push("/workspace");
    } else {
      errorMessage.value =
        props.mode === "login"
          ? "Неверный логин или пароль"
          : "Пользователь с таким логином уже существует";
    }
  } catch (error) {
    errorMessage.value = "Произошла ошибка. Попробуйте позже";
    console.error("Auth error:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped lang="scss">
.modal-overlay {
  background-color: #000a1dc1;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

  .modal-content {
    width: 550px;
    height: 400px;
    background-color: var(--shadow-background);
    backdrop-filter: blur(7px);
    -webkit-backdrop-filter: blur(7px);
    color: var(--text-color);
    border-radius: 12px;
    padding: 30px 20px;
    max-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    font-size: 22px;

    .close-btn {
      position: absolute;
      top: 10px;
      right: 15px;
      background: none;
      border: none;
      font-size: 22px;
      color: var(--text-color);
      cursor: pointer;
    }

    form {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 20px;

      .form-group {
        display: flex;
        flex-direction: column;
        gap: 20px;

        ::placeholder {
          color: white;
        }

        ::-webkit-input-placeholder {
          color: white;
        }

        input {
          background-color: grey;
          padding: 5px 20px;
          border-radius: 10px;
          color: white;
        }
      }

      button {
        display: flex;
        align-items: center;
        height: 40px;
        position: relative;
        overflow: hidden;
        z-index: 0;
        background-color: var(--shadow-background);
        padding: 5px 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        cursor: pointer;

        &::before {
          content: "";
          position: absolute;
          top: 0;
          left: -60%;
          width: 40%;
          height: 100%;
          background: linear-gradient(120deg,
              rgba(255, 255, 255, 0) 0%,
              rgba(255, 255, 255, 0.4) 50%,
              rgba(255, 255, 255, 0) 100%);
          transform: skewX(-20deg);
          animation: shine 3s ease-in-out infinite;
          z-index: 1;
          pointer-events: none;
        }
      }
    }
  }
}
</style>
