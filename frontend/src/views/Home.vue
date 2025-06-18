<template>
  <div class="home">
    <h2 v-if="username">{{ username }}さんのタスク管理</h2>
    <LoadingSpinner v-else />
    <button @click="showModal = true" class="create-btn">タスク作成</button>
    <TaskCreateModal v-if="showModal" @close="showModal = false" @success="onCreated" />
  </div>
</template>

<script>
import axios from 'axios'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import TaskCreateModal from '@/components/TaskCreateModal.vue'

export default {
  name: 'HomePage',
  components: {
    LoadingSpinner,
    TaskCreateModal
  },
  data() {
    return {
      username: null,
      showModal: false
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
  },
  methods: {
    onCreated() {
      alert("タスクが作成されました")
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
.create-btn {
  margin-top: 20px;
  padding: 10px 15px;
  font-size: 1rem;
  background-color: #a77bc2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
