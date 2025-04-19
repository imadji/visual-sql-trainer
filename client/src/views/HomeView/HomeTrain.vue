<template>
    <div class="train-container">
        <div class="train-text">
            <label>Тренируй свои навыки</label>
            <span>SQL — это навык, который лучше всего развивается в практике.
                Внутри тебя ждут интерактивные задания, живые примеры и понятные объяснения.
                От простых SELECT до сложных JOIN и подзапросов — ты сам решаешь темп и направление.
                Попробуй — и поймешь, что учиться можно интересно.
            </span>
        </div>
        <!-- <div class="train-photo"></div> -->
        <img src="../../assets/train-image.png" alt="">
    </div>
</template>

<script setup>
// Никаких реактивностей не нужно — кнопка просто эмитит событие
</script>

<style scoped lang="scss">
.train-container {
    width: 100%;
    margin-top: 100px;
    margin-bottom: 150px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;

    .train-text {
        display: flex;
        flex-direction: column;

        label {
            font-size: 42px;
            margin-bottom: 15px;
        }

        span {
            font-size: 20px;
        }
    }

    img {
        width: 500px;
        background-color: #fff;
        border-radius: 10px;
    }
}

/* Small (sm) – устройства от 576px */
@media (max-width: 576px) {
    .train-container {
        margin-bottom: 150px !important;
        gap: 50px;
        flex-direction: column;

        .train-text {
            label {
                font-size: 25px !important;
            }

            span {
                font-size: 18px !important;
            }
        }
    }
}

/* Medium (md) – устройства от 768px */
@media (max-width: 768px) {
    .train-container {
        margin-bottom: 150px;
        gap: 50px;
        flex-direction: column;

        .train-text {
            label {
                font-size: 33px !important;
            }

            span {
                font-size: 18px !important;
            }
        }
    }
}

/* Large (lg) – устройства от 992px */
@media (max-width: 992px) {
    .train-container {
        margin-bottom: 50px;
        gap: 50px;
        flex-direction: column;

        .train-text {
            label {
                font-size: 37px;
            }

            span {
                font-size: 18px;
            }
        }
    }
}
</style>