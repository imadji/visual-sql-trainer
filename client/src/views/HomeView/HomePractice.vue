<template>
    <div class="practice-container">
        <label>Учись на практике</label>
        <div class="practice-info">
            <img src="../../assets/practice-image.png" alt="">
            <span>Никакой установки и лишней теории — только реальные задачи, консоль и мгновенный результат. Ошибся?
                Попробуй снова. Учись в действии.
            </span>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from "vue";
import { gsap } from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

onMounted(() => {
    gsap.from(".practice-container", {
        xPercent: 20,
        opacity: 0,
        duration: 1.2,
        ease: "power3.out",
        scrollTrigger: {
            trigger: ".practice-container",
            start: "top bottom",
            toggleActions: "play none none none",
        },
    });
});
</script>


<style scoped lang="scss">
.practice-container {
    width: 100%;
    margin-top: 100px;
    display: flex;
    flex-direction: column;
    gap: 15px;

    label {
        display: flex;
        font-size: 42px;
        margin-bottom: 15px;
    }

    span {
        font-size: 20px;
    }

    .practice-info {
        display: flex;
        justify-content: space-between;
        gap: 50px;

        img {
            width: 800px;
        }
    }
}

/* Small (sm) – устройства от 576px */
@media (max-width: 576px) {
    .practice-container {
        .practice-info {
            img {
                width: 450px;
            }
        }
    }
}

/* Large (lg) – устройства от 992px */
@media (max-width: 992px) {
    .practice-container {
        .practice-info {
            flex-direction: column;

            span {
                font-size: 18px;
            }
        }
    }
}
</style>