<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <button @click="prevMonth">‹</button>
      <h3>{{ year }}年{{ month }}月</h3>
      <button @click="nextMonth">›</button>
    </div>
    <div class="calendar-grid">
      <div class="calendar-day" v-for="day in weekDays" :key="day">{{ day }}</div>
      <div v-for="blank in startDay" :key="'blank-' + blank" class="calendar-cell empty"></div>
      <div v-for="date in daysInMonth" :key="date" class="calendar-cell">
        <div class="date-number">{{ date }}</div>
        <ul class="task-list">
          <li
            v-for="task in tasksByDate[formatDate(year, month, date)]"
            :key="task.id"
            class="task-item"
            @click="openTask(task)"
          >
            {{ task.name }}
          </li>
        </ul>
      </div>
    </div>

    <div v-if="selectedTask" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>{{ selectedTask.name }}</h3>
        <p><strong>優先度:</strong> {{ priorityLabel(selectedTask.priority) }}</p>
        <p><strong>ステータス:</strong> {{ statusLabel(selectedTask.status) }}</p>
        <p><strong>説明:</strong> {{ selectedTask.description || '説明なし' }}</p>
        <button @click="editTask">編集</button>
        <button @click="closeModal">閉じる</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)
const tasks = ref([])
const selectedTask = ref(null)

const weekDays = ['日', '月', '火', '水', '木', '金', '土']

const daysInMonth = computed(() => new Date(year.value, month.value, 0).getDate())
const startDay = computed(() => new Date(year.value, month.value - 1, 1).getDay())

function formatDate(y, m, d) {
  return `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`
}

const tasksByDate = computed(() => {
  const map = {}
  tasks.value.forEach(task => {
    const date = task.deadline
    if (!map[date]) map[date] = []
    map[date].push(task)
  })
  return map
})

async function fetchTasks() {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const res = await axios.get('http://localhost:8000/task_management/tasks/task_lists/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    tasks.value = res.data
  } catch (e) {
    console.error('タスク取得エラー', e)
  }
}
console.log(tasks);

function prevMonth() {
  if (month.value === 1) {
    year.value--
    month.value = 12
  } else {
    month.value--
  }
  fetchTasks()
}

function nextMonth() {
  if (month.value === 12) {
    year.value++
    month.value = 1
  } else {
    month.value++
  }
  fetchTasks()
}

function openTask(task) {
  selectedTask.value = task
}

function closeModal() {
  selectedTask.value = null
}

function editTask() {
  // 後で実装予定: 編集モーダルや遷移
  alert(`編集画面（仮）: ${selectedTask.value.name}`)
}

function priorityLabel(val) {
  return { high: '高', medium: '中', low: '低' }[val] || val
}
function statusLabel(val) {
  return {
    not_started: '未着手',
    in_progress: '進行中',
    completed: '完了'
  }[val] || val
}

onMounted(fetchTasks)
</script>

<style scoped>
.calendar-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}
.calendar-day {
  text-align: center;
  font-weight: bold;
  padding: 5px;
}
.calendar-cell {
  border: 1px solid #ccc;
  padding: 5px;
  min-height: 80px;
  background-color: #f9f9f9;
}
.calendar-cell .date-number {
  font-weight: bold;
}
.task-list {
  list-style: none;
  padding: 0;
  margin: 5px 0 0 0;
}
.task-item {
  font-size: 12px;
  background-color: #a77bc2;
  color: white;
  margin: 2px 0;
  padding: 2px 4px;
  border-radius: 4px;
  cursor: pointer;
}
.empty {
  background: transparent;
  border: none;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  max-width: 400px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
.modal button {
  margin-top: 10px;
  margin-right: 10px;
  background-color: #a77bc2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
