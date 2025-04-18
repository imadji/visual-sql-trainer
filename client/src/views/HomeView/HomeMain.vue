<template>
    <main class="main-container">
        <img ref="logo" class="logo" src="../../assets/big-logo.png" alt="">
        <span>
            <div class="main-label-text-title">SQL Coding</div>
            <div class="main-label-text-semititle">SQL Coding - Просто. Чётко. Работает.</div>
            <div class="main-label-text">Учись писать SQL - запросы быстро и просто.</div>
            <div class="main-label-text">Пробуй, ошибайся, улучшай! </div>
            <button @click="startTraining">Начать тренировку</button>
        </span>
        <img class="back-text" src="../../assets/title-text.png" alt="">
    </main>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { gsap } from "gsap";
import { useRouter } from "vue-router";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const router = useRouter();
const logo = ref(null);
const mainContainer = ref(null);
gsap.registerPlugin(ScrollTrigger);

const startTraining = () => {
    router.push("/workspace");
};

onMounted(() => {
    gsap.from(".main-label-text-title", { duration: 1, y: -50, opacity: 0, ease: "power2.out" });
    gsap.from(".main-label-text-semititle", { duration: 1.2, y: -40, opacity: 0, delay: 0.3, ease: "power2.out" });
    gsap.from(".main-label-text", {
        duration: 1,
        opacity: 0,
        stagger: 0.2,
        delay: 0.6,
        ease: "power2.out"
    });
    gsap.from("button", { duration: 1, scale: 0.8, opacity: 0, delay: 1, ease: "back.out(1.7)" });

    if (logo.value) {
        gsap.to(logo.value, {
            x: 200,
            y: 100,
            scale: 0.8,
            rotation: 10,
            scrollTrigger: {
                trigger: mainContainer.value,
                start: "top top",
                end: "bottom top",
                scrub: 1,
                markers: false,
                ease: "power1.out"
            }
        });
    }
});

onUnmounted(() => {
    ScrollTrigger.getAll().forEach(trigger => trigger.kill());
});
</script>


<style scoped lang="scss">
.main-container {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 10px;

    .back-text {
        position: absolute;
        width: 60%;
        z-index: 0;
    }

    .logo {
        z-index: 1;
        backdrop-filter: blur(2px);
        // will-change: transform;
    }

    span {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        z-index: 2;

        .main-label-text-title {
            margin-bottom: 20px;
            font-size: 63px;
            font-weight: 900;
            padding: 0 20px;
            background-color: rgba(214, 214, 214, 0.3);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transform: translateX(-80px);
            backdrop-filter: blur(2px);
        }

        .main-label-text-semititle {
            font-size: 37px;
            transform: translateX(-30px);
        }

        .main-label-text {
            font-size: 20px;
        }

        button {
            margin-top: 30px;
            position: relative;
            overflow: hidden;
            z-index: 0;
            background-color: var(--shadow-background);
            padding: 15px 40px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            cursor: pointer;
            font-size: 25px;
            backdrop-filter: blur(2px);

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
                pointer-events: none; // чтобы не мешать кликам
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

    }
}

/* Small (sm) – устройства от 576px */
@media (max-width: 576px) {
    .main-container {
        img {
            opacity: 0.5;
            filter: blur(5px);
        }

        span {
            transform: translateX(20px) !important;

            .main-label-text-title {
                font-size: 30px !important;
                transform: translateX(0) !important;
            }

            .main-label-text-semititle {
                font-size: 18px !important;
                transform: translateX(0) !important;
            }

            .main-label-text {
                font-size: 16px !important;
                transform: translateX(0) !important;
            }
        }
    }
}

/* Medium (md) – устройства от 768px */
@media (max-width: 768px) {
    .main-container {
        img {
            position: absolute;
            opacity: 0.5;
            filter: blur(5px);
        }

        span {
            transform: translateX(none);

            .main-label-text-title {
                font-size: 37px;
                transform: translateX(0) !important;
            }

            .main-label-text-semititle {
                font-size: 18px;
                transform: translateX(0) !important;
            }

            .main-label-text {
                font-size: 16px;
                transform: translateX(0) !important;
            }
        }
    }
}

/* Large (lg) – устройства от 992px */
@media (max-width: 992px) {
    .main-container {
        span {
            .main-label-text-title {
                // font-size: 53px;
            }

            .main-label-text-semititle {
                font-size: 27px;
            }

            .main-label-text {
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