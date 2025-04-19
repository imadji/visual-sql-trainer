<template>
  <header class="header-container">
    <span>
      <img src="../../assets/Logo-mini.png" alt="" />
      <label>SQL Coding</label>
    </span>
    <div class="sign-container">
      <button class="sign-up-btn" @click="$emit('open-auth', 'login')">Вход</button>
      <button class="sign-up-btn" @click="$emit('open-auth', 'register')">Регистрация</button>
    </div>
  </header>
</template>


<script scoped setup>
import { onMounted } from "vue";
import { gsap } from "gsap";

onMounted(() => {
    gsap.from("span", { duration: 1, y: -50, opacity: 0, ease: "power2.out" });
    // gsap.from("button", { duration: 1, scale: 0.8, opacity: 0, delay: 1, ease: "back.out(1.7)" });
});
</script>

<style scoped lang="scss">
.header-container {
  width: 100vw;
  padding-top: 20px;
  // height: 10vh;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  position: fixed;
  background-color: var(--background-color);
  // backdrop-filter: blur(10px);
  z-index: 999;
  left: 0;
  right: 0;
  top: 0;
  padding: 20px 40px;

  span {
    display: flex;
    align-items: center;
  }

  label {
    font-size: 26px;
    font-weight: 500;
    transform: translateX(-10px);
  }

  .sign-container {
    display: flex;
    flex-direction: row;
    gap: 10px;

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

  @keyframes shine {
    0% {
      left: -60%;
    }

    100% {
      left: 120%;
    }
  }

  /* Small (sm) – устройства от 576px */
}

@media (max-width: 456px) {
  .header-container {
    .sign-container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>
