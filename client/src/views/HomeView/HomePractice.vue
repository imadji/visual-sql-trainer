<template>
    <div class="practice-container">
        <div class="practice-text">
            <label>Учись на практике</label>
            <span>Никакой установки и лишней теории — только реальные задачи, консоль и мгновенный результат. Ошибся? Попробуй снова. Учись в действии.
            </span>
        </div>
        <div class="practice-photo"></div>
    </div>
</template>

<script setup>
  // Никаких реактивностей не нужно — кнопка просто эмитит событие
</script>

<style scoped lang="scss">
.practice-container{
    width: 100%;
    margin-top: 100px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;

    .practice-text{
    display: flex;
    flex-direction: column;
    label{
    font-size: 42px;
    margin-bottom: 15px;
    }
    span{
    font-size: 20px;
    }
}
}

/* Small (sm) – устройства от 576px */
@media (max-width: 576px) {
}

/* Medium (md) – устройства от 768px */
@media (max-width: 768px) {
}

/* Large (lg) – устройства от 992px */
@media (max-width: 992px) {
}
</style>