<template>
  <div class="home">
    <h2 v-if="username">{{ username }}さんのタスク管理</h2>
    <p v-else>ユーザー情報を取得中...</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomePage',
  data() {
    return {
      username: null,
    }
  },
  async created() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const response = await axios.get('http://localhost:8000/accounts/user/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.username = response.data.username
        console.log(response.data)
      } catch (e) {
        console.error('ユーザー取得エラー:', e)
        this.username = 'ゲスト'
      }
    } else {
      this.username = 'ゲスト'
    }
  }
}
</script>

<style scoped>
.home {
  margin-top: 40px;
  font-size: 1.5rem;
  color: #a77bc2; /* メインカラーに合わせた装飾 */
}
</style>
