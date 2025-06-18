<template>
    <div class="auth-container">
        <h2>Login</h2>
        <form @submit.prevent="login">
        <div class="form-group">
            <label>Username:</label>
            <input v-model="username" required />
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
        </form>
        <p v-if="error" style="color:red;">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'UserLogin',
    data() {
        return {
        username: '',
        password: '',
        error: null
        }
    },
    methods: {
        async login() {
        try {
            this.error = null
            const response = await axios.post('http://localhost:8000/accounts/login/', {
            username: this.username,
            password: this.password
            })
            const { access, refresh } = response.data
            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)
            // ログイン後の画面遷移やトークン利用はここに実装
            this.$router.push('/home')
        } catch (e) {
            this.error = e.response?.data?.detail || 'Login failed'
        }
        }
    }
}
</script>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 80px auto;
    padding: 30px;
    border-radius: 12px;
    background-color: #e6d2f3; /* サブカラー */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
    color: #a77bc2; /* メインカラー */
    text-align: center;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 6px;
    color: #4a4a4a;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #a77bc2; /* メインカラー */
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #8f62ad;
}

.error-msg {
    color: red;
    margin-top: 10px;
    text-align: center;
}
</style>