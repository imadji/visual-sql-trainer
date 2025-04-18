<template>
    <main class="main-container">
      <img src="../../assets/big-logo.png" alt="">
      <span>
        <div class="main-label-text-title">SQL Coding</div>
        <div class="main-label-text-semititle">SQL Coding - Просто. Чётко. Работает.</div>
        <div class="main-label-text">Учись писать SQL-запросы быстро и просто.</div>
        <div class="main-label-text">Пробуй, ошибайся, улучшай! </div>
      </span>
    </main>
</template>

<script setup>
    // Никаких реактивностей не нужно — кнопка просто эмитит событие
</script>

<style scoped lang="scss">
.main-container{
width: 100%;
height: 100%;
display: flex;
flex-direction: row;
align-items: center;
justify-content: center;
gap: 10px;

    span{
    display: flex;
    flex-direction: column;
    align-items: flex-start;

        .main-label-text-title{
            font-size: 63px;
            font-weight: 900;
            padding: 0 20px;
            background-color: rgba(214, 214, 214, 0.3);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transform: translateX(-60px);
        }
        .main-label-text-semititle{
            font-size: 37px;
            transform: translateX(-30px);
        }
        .main-label-text{
            font-size: 20px;
        }
    }
}
</style>