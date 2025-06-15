<template>
    <div>
        <h2>Signup</h2>
        <form @submit.prevent="signup">
        <div>
            <label>Username:</label>
            <input v-model="username" required />
        </div>
        <div>
            <label>Password:</label>
            <input type="password" v-model="password" required />
        </div>
        <button type="submit">Sign Up</button>
        </form>
        <p v-if="error" style="color:red;">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'UserSignup',
    data() {
        return {
        username: '',
        password: '',
        error: null
        }
    },
    methods: {
        async signup() {
        try {
            this.error = null
            await axios.post('http://localhost:8000/accounts/signup/', {
            username: this.username,
            password: this.password
            })
            alert('Signupが完了しました')
            this.$router.push('/login')  // ← ここでログイン画面へ遷移
        } catch (e) {
            this.error = e.response?.data?.detail || 'Signup failed'
        }
        }
    }
}
</script>
