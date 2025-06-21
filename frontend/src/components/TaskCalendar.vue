
<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <button @click="prevMonth">‹</button>
      <h3>{{ year }}年{{ month }}月</h3>
      <button @click="nextMonth">›</button>
    </div>
    <div class="calendar-grid">
      <div class="calendar-day" v-for="day in weekDays" :key="day">{{ day }}</div>
      <div
        v-for="blank in startDay"
        :key="'blank-' + blank"
        class="calendar-cell empty"
      ></div>
      <div
        v-for="date in daysInMonth"
        :key="date"
        class="calendar-cell"
      >
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1) // 1-12

const tasks = ref([])

const weekDays = ['日', '月', '火', '水', '木', '金', '土']

const daysInMonth = computed(() => {
  return new Date(year.value, month.value, 0).getDate()
})

const startDay = computed(() => {
  return new Date(year.value, month.value - 1, 1).getDay()
})

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
    const res = await axios.get(
      `http://localhost:8000/task_management/tasks/task_lists/`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    tasks.value = res.data
  } catch (e) {
    console.error('タスク取得エラー', e)
  }
}

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
  alert(`[タスク詳細]
名前: ${task.name}
期限: ${task.deadline}`)
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
</style>
