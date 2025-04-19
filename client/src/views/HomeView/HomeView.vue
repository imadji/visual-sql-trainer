<template>
  <div class="wrapper">
    <div class="container">
      <HomeHeader @open-auth="showAuthModal" />
      <HomeMain />
      <hr />
      <HomeTrain />
      <HomePractice />
      <HomeFooter />
    </div>
    <AuthModal v-if="isModalVisible" :mode="modalMode" @close="hideAuthModal" />
  </div>
</template>

<script setup>
import { onUnmounted, ref, watchEffect } from "vue";
import AuthModal from "@/components/AuthModal.vue";
import HomeHeader from "./HomeHeader.vue";
import HomeMain from "./HomeMain.vue";
import HomeTrain from "./HomeTrain.vue";
import HomeFooter from "./HomeFooter.vue";
import HomePractice from "./HomePractice.vue";

const isModalVisible = ref(false);
const modalMode = ref("login");

const showAuthModal = (mode) => {
  modalMode.value = mode;
  isModalVisible.value = true;
};

const hideAuthModal = () => {
  isModalVisible.value = false;
};

watchEffect(() => {
  if (isModalVisible.value) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "";
  }
});

onUnmounted(() => {
  document.body.style.overflow = "";
});
</script>

<style lang="scss" scoped>
.wrapper{
  width: 100%;
  height: 100%;
  position: relative;
}

.container {
  display: flex;
  flex-direction: column;
  // height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  padding-left: 2%;
  padding-right: 2%;
  padding-top: 20px;
  position: relative;
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
