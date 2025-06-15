<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
        <div>
            <label>Username:</label>
            <input v-model="username" required />
        </div>
        <div>
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
            alert('ログインしました')
            // ログイン後の画面遷移やトークン利用はここに実装
        } catch (e) {
            this.error = e.response?.data?.detail || 'Login failed'
        }
        }
    }
}
</script>
