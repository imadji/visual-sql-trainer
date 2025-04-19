<template>
    <div class="practice-container">
        <!-- <div class="practice-text"> -->
            <label>Учись на практике</label>
            <div class="practice-info">
                <img src="../../assets/practice-image.png" alt="">
                <span>Никакой установки и лишней теории — только реальные задачи, консоль и мгновенный результат. Ошибся? Попробуй снова. Учись в действии.
                </span>
            </div>
        <!-- </div> -->
        <!-- <div class="practice-photo"></div> -->
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
    flex-direction: column;
    // align-items: center;
    // justify-content: space-between;
    gap: 15px;


    label{
        display: flex;
        // align-items: flex-start;
        // justify-content: flex-start;
        font-size: 42px;
        margin-bottom: 15px;
    }

    span{
    font-size: 20px;
    }

    .practice-info{
        display: flex;
        justify-content: space-between;

        img{
            width: 600px;
        }
    }

    // .practice-text{
    // display: flex;
    // flex-direction: column;
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