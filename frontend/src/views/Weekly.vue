<template>
  <div class="home">
    <div class="header" v-if="username">
      <h2>{{ username }}さんの週次タスク</h2>
      <button class="create-btn" @click="showCreateModal = true">週次タスク作成</button>
    </div>
    <LoadingSpinner v-else />

    <WeeklyCreateModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="fetchTasks"
    />

    <div v-if="username" class="week-container">
      <div v-for="day in weekdays" :key="day.key" class="weekday-column">
        <h3 class="weekday-title">{{ day.label }}</h3>
        <div v-if="tasksByDay[day.key]?.length" class="task-list">
          <div
            v-for="task in tasksByDay[day.key]"
            :key="task.id"
            class="task-card"
            @click="openTask(task)"
          >
            <div class="card-header">
              <h4 class="task-name">{{ task.name }}</h4>
              <span class="priority-badge" :class="task.priority">{{ priorityLabel(task.priority) }}</span>
            </div>
            <p class="description">{{ task.description || '（説明なし）' }}</p>
          </div>
        </div>
        <p v-else class="no-task">タスクなし</p>
      </div>
    </div>

    <WeeklyEditModal
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
import WeeklyEditModal from '@/components/WeeklyEditModal.vue'
import WeeklyCreateModal from '@/components/WeeklyCreateModal.vue'

export default {
  name: 'WeeklyTask',
  components: {
    LoadingSpinner,
    WeeklyEditModal,
    WeeklyCreateModal,
  },
  data() {
    return {
      username: null,
      tasks: [],
      weekdays: [
        { key: 'mon', label: '月曜日' },
        { key: 'tue', label: '火曜日' },
        { key: 'wed', label: '水曜日' },
        { key: 'thu', label: '木曜日' },
        { key: 'fri', label: '金曜日' },
        { key: 'sat', label: '土曜日' },
        { key: 'sun', label: '日曜日' },
      ],
      selectedTask: null,
      showCreateModal: false
    }
  },
  computed: {
    tasksByDay() {
      const result = {
        mon: [], tue: [], wed: [], thu: [],
        fri: [], sat: [], sun: []
      }

      const priorityOrder = { high: 0, medium: 1, low: 2 }

      this.tasks.forEach(task => {
        if (task.repeat_rule?.frequency === 'weekly') {
          const days = task.repeat_rule.days || [task.repeat_rule.day]
          days.forEach(day => {
            const key = this.normalizeDay(day)
            if (result[key]) result[key].push(task)
          })
        }
      })

      Object.keys(result).forEach(day => {
        result[day].sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority])
      })

      return result
    }
  },
  async created() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const responseUser = await axios.get('http://localhost:8000/accounts/user/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.username = responseUser.data.username
        await this.fetchTasks()
      } catch (e) {
        console.error('取得エラー:', e)
        this.username = 'ゲスト'
      }
    } else {
      this.username = 'ゲスト'
    }
  },
  methods: {
    priorityLabel(val) {
      return { high: '高', medium: '中', low: '低' }[val] || val
    },
    normalizeDay(day) {
      const map = {
        monday: 'mon', tuesday: 'tue', wednesday: 'wed',
        thursday: 'thu', friday: 'fri', saturday: 'sat', sunday: 'sun',
        mon: 'mon', tue: 'tue', wed: 'wed', thu: 'thu', fri: 'fri', sat: 'sat', sun: 'sun'
      }
      return map[day.toLowerCase()]
    },
    openTask(task) {
      this.selectedTask = { ...task }
    },
    async fetchTasks() {
      const token = localStorage.getItem('access_token')
      if (!token) return
      try {
        const response = await axios.get('http://localhost:8000/task_management/weekly/weekly_task_lists/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.tasks = response.data
      } catch (error) {
        console.error('週次タスク取得エラー:', error)
      }
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

.week-container {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.weekday-column {
  min-width: 140px;
  background: #f8f4fa;
  border-radius: 10px;
  padding: 12px;
  box-sizing: border-box;
}

.weekday-title {
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  color: #6b4b99;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-card {
  background: white;
  border-left: 6px solid #a77bc2;
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-name {
  margin: 0;
  font-size: 1rem;
}

.priority-badge {
  padding: 2px 6px;
  border-radius: 10px;
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
  margin-top: 6px;
  font-size: 0.85rem;
  color: #555;
}

.no-task {
  font-size: 0.9rem;
  color: #999;
  text-align: center;
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
