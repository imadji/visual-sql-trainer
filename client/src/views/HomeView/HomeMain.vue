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
</script>

<style scoped lang="scss">
.main-container{
width: 100%;
height: 90vh;
display: flex;
flex-direction: row;
align-items: center;
justify-content: center;
gap: 10px;

    img{
        z-index: 0;
    }
    span{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    z-index: 1;

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

/* Small (sm) – устройства от 576px */
@media (max-width: 576px) {
    .main-container{
        img{
            opacity: 0.5;
            filter: blur(5px);
        }
        span{
            transform: translateX(20px) !important;
            .main-label-text-title{
                font-size: 30px !important;
                transform: translateX(0) !important;
            }
            .main-label-text-semititle{
                font-size: 18px !important;
                transform: translateX(0) !important;
            }
            .main-label-text{
                font-size: 16px !important;
                transform: translateX(0) !important;
            }
        }
    }}

/* Medium (md) – устройства от 768px */
@media (max-width: 768px) {
    .main-container{
        img{
            position: absolute;
            opacity: 0.5;
            filter: blur(5px);
        }
        span{
            transform: translateX(none);
            .main-label-text-title{
                font-size: 37px;
                transform: translateX(0) !important;
            }
            .main-label-text-semititle{
                font-size: 18px;
                transform: translateX(0) !important;
            }
            .main-label-text{
                font-size: 16px;
                transform: translateX(0) !important;
            }
        }
    }
}

/* Large (lg) – устройства от 992px */
@media (max-width: 992px) {
    .main-container{
        span{
            .main-label-text-title{
                // font-size: 53px;
            }
            .main-label-text-semititle{
                font-size: 27px;
            }
            .main-label-text{
                font-size: 20px;
            }
        }
    }
}

/* Extra large (xl) – устройства от 1200px */
@media (max-width: 1200px) {
  /* Стили для экранов шириной ≥ 1200px */
}

/* Extra extra large (xxl) – устройства от 1400px */
@media (max-width: 1400px) {
  /* cтили для экранов шириной ≥ 1400px */
}
</style>