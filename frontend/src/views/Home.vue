<template>
  <div class="home">
    <div class="header" v-if="username">
      <h2 class="title">{{ username }}さんのタスク管理</h2>
      <button @click="showModal = true" class="create-btn">タスク作成</button>
    </div>
    <LoadingSpinner v-else />
    <TaskCreateModal v-if="showModal" @close="showModal = false" @success="onCreated" />
    <TaskCalendar/>
  </div>
</template>

<script>
import axios from 'axios'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import TaskCreateModal from '@/components/TaskCreateModal.vue'
import TaskCalendar from '@/components/TaskCalendar.vue'

export default {
  name: 'HomePage',
  components: {
    LoadingSpinner,
    TaskCreateModal,
    TaskCalendar
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
  margin-top: 10px;
  font-size: 1.5rem;
  color: #a77bc2;
}

.header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title {
  font-size: 2rem;
  color: #a77bc2;
}

.create-btn {
  padding: 8px 16px;
  font-size: 1rem;
  background-color: #a77bc2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
