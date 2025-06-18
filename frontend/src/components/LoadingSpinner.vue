<!-- src/components/LoadingSpinner.vue -->
<template>
    <div class="spinner-container">
        <div class="spinner"></div>
    </div>
</template>

<script>
export default {
    name: 'LoadingSpinner'
}
</script>

<style scoped>
.spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 5px solid #e6d2f3; /* サブカラー */
    border-top: 5px solid #a77bc2; /* メインカラー */
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>
