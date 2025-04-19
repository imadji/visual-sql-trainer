<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <!-- добавить икноку закрытия -->
      <button class="close-btn" @click="close">Х</button>
      <h2>{{ mode === "login" ? "Вход" : "Регистрация" }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="login">Логин:</label>
          <input id="login" v-model="login" type="text" placeholder="Введите ваш логин" required />
        </div>

        <div class="form-group">
          <label for="password">Пароль:</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Введите пароль"
            required
          />
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

    if (response?.status) {
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

<style scoped lang="scss"></style>
