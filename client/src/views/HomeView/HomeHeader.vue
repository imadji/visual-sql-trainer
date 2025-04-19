<template>
    <header class="header-container">
        <span>
        <img src="../../assets/Logo-mini.png" alt="" />
        <label>SQL Coding</label>
        </span>
        <button class="sign-up-btn" @click="$emit('open-auth', 'login')">Вход</button>
    </header>
</template>

<script setup>
  // Никаких реактивностей не нужно — кнопка просто эмитит событие
</script>

<style scoped lang="scss">
.header-container {
width: 100%;
height: 10vh;
display: flex;
align-items: flex-start;
justify-content: space-between;

span {
    display: flex;
    align-items: center;
}

label {
    font-size: 26px;
    font-weight: 500;
    transform: translateX(-10px);
}

button {
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
    background: linear-gradient(
        120deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.4) 50%,
        rgba(255, 255, 255, 0) 100%
    );
    transform: skewX(-20deg);
    animation: shine 3s ease-in-out infinite;
    z-index: 1;
    pointer-events: none;
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


// button {
//     display: flex;
//     align-items: center;
//     height: 40px;
//     position: relative;
//     overflow: hidden;
//     z-index: 0;
//     background-color: var(--shadow-background);
//     padding: 5px 20px;
//     border-radius: 10px;
//     border: 1px solid rgba(255, 255, 255, 0.1);
//     color: white;
//     cursor: pointer;
// }
}
</style>