<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>{{ mode === "login" ? "Вход" : "Регистрация" }}</h2>
      <form>
        <button @click="close">закрыть</button>
        <!-- Кнока закрытия-->
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Пароль" required />
        <button @click="handleSubmit">Отправить</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const props = defineProps(["mode"]);
const emit = defineEmits(["close"]);

const email = ref<string>("");
const password = ref<string>("");
const authStore = useAuthStore();
const router = useRouter();

const close = async () => {
  emit("close");
};

const handleSubmit = async () => {
  await authStore.login({
    email: email.value,
    password: password.value,
  });
  emit("close");
  router.push("/workspace");
};
</script>
