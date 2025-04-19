<template>
  <div class="container">
    <HomeHeader @open-auth="showAuthModal"/>
    <AuthModal v-if="isModalVisible" :mode="modalMode" @close="hideAuthModal" />
    <HomeMain/>
    <hr/>
    <HomeTrain/>
    <HomePractice/>
    <HomeFooter/>
  </div>
</template>

<script setup>
import { ref } from "vue";
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
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  // height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  padding-left: 2%;
  padding-right: 2%;
  padding-top: 20px;
}

hr {
  height: 2px;
  border: 0;
  background: linear-gradient(90deg,rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 50%, rgba(255, 255, 255, 0) 100%);
}

</style>
