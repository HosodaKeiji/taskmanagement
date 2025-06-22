<template>
  <div class="home">
    <div class="header" v-if="username">
      <h2>{{ username }}さんの月次タスク</h2>
      <button class="create-btn" @click="showCreateModal = true">月次タスク作成</button>
    </div>
    <LoadingSpinner v-else />
    <div class="task-grid">
      <div v-for="task in tasks" :key="task.id" class="task-card" @click="selectedTask = task">
        <div class="card-header">
          <h3 class="task-name">{{ task.name }}</h3>
          <span class="priority-badge" :class="task.priority">{{ priorityLabel(task.priority) }}</span>
        </div>
        <p class="description">{{ task.description || '（説明なし）' }}</p>
      </div>
    </div>
    <MonthlyCreateModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="fetchTasks"
    />

    <MonthlyEditModal
      v-if="selectedTask"
      :task="selectedTask"
      @close="selectedTask = null"
      @updated="fetchTasks"
    />
  </div>
</template>

<script>
import axios from 'axios'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import MonthlyEditModal from '@/components/MonthlyEditModal.vue'
import MonthlyCreateModal from '@/components/MonthlyCreateModal.vue'

export default {
  name: 'MonthlyTask',
  components: {
    LoadingSpinner,
    MonthlyEditModal,
    MonthlyCreateModal
  },
  data() {
    return {
      username: null,
      showCreateModal: false,
      selectedTask: null,
      tasks: []
    }
  },
  async created() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const userRes = await axios.get('http://localhost:8000/accounts/user/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.username = userRes.data.username
        await this.fetchTasks()
      } catch (e) {
        console.error('ユーザー取得エラー:', e)
        this.username = 'ゲスト'
      }
    } else {
      this.username = 'ゲスト'
    }
  },
  methods: {
    async fetchTasks() {
      const token = localStorage.getItem('access_token')
      try {
        const res = await axios.get('http://localhost:8000/task_management/monthly/monthly_task/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.tasks = res.data
      } catch (e) {
        console.error('月次タスク取得エラー:', e)
      }
    },
    priorityLabel(val) {
      return { high: '高', medium: '中', low: '低' }[val] || val
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
  margin-bottom: 10px;
}

.create-btn {
  background-color: #a77bc2;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background-color: #935bb3;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.task-card {
  background: #fff;
  border: 1px solid #ddd;
  border-left: 6px solid #a77bc2;
  border-radius: 10px;
  padding: 16px;
  transition: box-shadow 0.3s;
  cursor: pointer;
}

.task-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-name {
  font-size: 1.2rem;
  margin: 0;
}

.priority-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  color: white;
}

.priority-badge.high {
  background: #e74c3c;
}

.priority-badge.medium {
  background: #f39c12;
}

.priority-badge.low {
  background: #2ecc71;
}

.description {
  font-size: 0.85rem;
  color: #555;
  margin-top: 10px;
}

</style>
