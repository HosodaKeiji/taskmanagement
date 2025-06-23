<template>
  <div class="home">
    <div class="header" v-if="username">
      <h2 v-if="username">{{ username }}さんの日次タスク</h2>
      <button @click="showCreateModal = true" class="create-btn">日次タスク作成</button>
    </div>
    <LoadingSpinner v-else />
    <DailyCreateModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="fetchTasks"
    />
    <div class="task-grid" v-if="tasks.length">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-card"
        @click="openTask(task)"
      >
        <div class="card-header">
          <h3 class="task-name">{{ task.name }}</h3>
          <span class="priority-badge" :class="task.priority">{{ priorityLabel(task.priority) }}</span>
        </div>
        <p class="description">{{ task.description || '（説明なし）' }}</p>
      </div>
    </div>

    <DailyEditModal
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
import DailyEditModal from '@/components/DailyEditModal.vue'
import DailyCreateModal from '@/components/DailyCreateModal.vue'

export default {
  name: 'DailyTask',
  components: {
    LoadingSpinner,
    DailyEditModal,
    DailyCreateModal,
  },
  data() {
    return {
      username: null,
      tasks: [],
      selectedTask: null,
      showCreateModal: false
    }
  },
  async created() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const response = await axios.get('http://localhost:8000/accounts/user/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.username = response.data.username
        this.fetchTasks()
      } catch (e) {
        console.error('ユーザー取得エラー:', e)
        this.username = 'ゲスト'
      }
    }
  },
  methods: {
    async fetchTasks() {
      const token = localStorage.getItem('access_token')
      try {
        const res = await axios.get('http://localhost:8000/task_management/daily/daily_task_lists/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        // 日次タスクだけ抽出
        const dailyTasks = res.data

        // 優先度でソート（high > medium > low）
        const priorityOrder = { high: 0, medium: 1, low: 2 }
        dailyTasks.sort((a, b) => {
          return priorityOrder[a.priority] - priorityOrder[b.priority]
        })

        this.tasks = dailyTasks
      } catch (e) {
        console.error('タスク取得エラー:', e)
      }
    },
    priorityLabel(val) {
      return { high: '高', medium: '中', low: '低' }[val] || val
    },
    openTask(task) {
      this.selectedTask = { ...task }
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
</style>
