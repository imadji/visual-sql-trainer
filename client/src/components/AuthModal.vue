<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>{{ mode === "login" ? "Вход" : "Регистрация" }}</h2>
      <form @submit.prevent="handleSubmit">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Пароль" required />
        <button type="submit">Отправить</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const props = defineProps(["mode"]);
const emit = defineEmits(["close"]);

const email = ref("");
const password = ref("");
const authStore = useAuthStore();
const router = useRouter();

const handleSubmit = async () => {
  await authStore.login({
    email: email.value,
    password: password.value,
  });
  emit("close");
  router.push("/workspace");
};
</script>
