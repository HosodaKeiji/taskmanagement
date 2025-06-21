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
            :class="{
              'high-priority': task.priority === 'high',
              'completed': task.status === 'completed'
            }"
            @click="openTask(task)"
          >
            <span v-if="task.status === 'in_progress'">▶ </span>{{ task.name }}
          </li>
        </ul>
      </div>
    </div>

    <div v-if="selectedTask" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>
          <template v-if="isEditing">
            <input class="modal-input" v-model="selectedTask.name" />
          </template>
          <template v-else>
            {{ selectedTask.name }}
          </template>
        </h3>

        <p>
          <strong>優先度:</strong>
          <template v-if="isEditing">
            <select class="modal-select" v-model="selectedTask.priority">
              <option value="high">高</option>
              <option value="medium">中</option>
              <option value="low">低</option>
            </select>
          </template>
          <template v-else>
            {{ priorityLabel(selectedTask.priority) }}
          </template>
        </p>

        <p>
          <strong>ステータス:</strong>
          <template v-if="isEditing">
            <select class="modal-select" v-model="selectedTask.status">
              <option value="not_started">未着手</option>
              <option value="in_progress">進行中</option>
              <option value="completed">完了</option>
            </select>
          </template>
          <template v-else>
            {{ statusLabel(selectedTask.status) }}
          </template>
        </p>

        <p>
          <strong>説明:</strong><br />
          <template v-if="isEditing">
            <textarea class="modal-textarea" v-model="selectedTask.description" rows="3" />
          </template>
          <template v-else>
            {{ selectedTask.description || '説明なし' }}
          </template>
        </p>

        <div class="modal-buttons">
          <template v-if="isEditing">
            <button class="submit-btn" @click="saveTaskEdits">保存</button>
            <button class="cancel-btn" @click="isEditing = false">キャンセル</button>
          </template>
          <template v-else>
            <button @click="advanceStatus" class="status-btn">
              {{ nextStatusLabel }}
            </button>
            <button class="submit-btn" @click="editTask">編集</button>
            <button class="cancel-btn" @click="closeModal">閉じる</button>
          </template>
        </div>
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

  const totalDays = daysInMonth.value

  tasks.value.forEach(task => {
    if (task.deadline) {
      const date = task.deadline
      if (!map[date]) map[date] = []
      map[date].push(task)
    } else if (task.repeat_rule) {
      const rule = task.repeat_rule
      const currentYear = year.value
      const currentMonth = month.value

      if (rule.frequency === 'weekly' && rule.day) {
        const dayMap = {
          sunday: 0,
          monday: 1,
          tuesday: 2,
          wednesday: 3,
          thursday: 4,
          friday: 5,
          saturday: 6
        }
        const targetWeekday = dayMap[rule.day.toLowerCase()]
        if (targetWeekday === undefined) return

        for (let d = 1; d <= totalDays; d++) {
          const dateObj = new Date(currentYear, currentMonth - 1, d)
          if (dateObj.getDay() === targetWeekday) {
            const dateStr = formatDate(currentYear, currentMonth, d)
            if (!map[dateStr]) map[dateStr] = []
            map[dateStr].push(task)
          }
        }
      }

      if (rule.frequency === 'monthly' && rule.day) {
        const dayNum = parseInt(rule.day)
        if (dayNum >= 1 && dayNum <= totalDays) {
          const dateStr = formatDate(currentYear, currentMonth, dayNum)
          if (!map[dateStr]) map[dateStr] = []
          map[dateStr].push(task)
        }
      }

      if (rule.frequency === 'daily') {
        for (let d = 1; d <= totalDays; d++) {
          const dateStr = formatDate(currentYear, currentMonth, d)
          if (!map[dateStr]) map[dateStr] = []
          map[dateStr].push(task)
        }
      }
    }
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

const isEditing = ref(false)

function editTask() {
  isEditing.value = true
}

function saveTaskEdits() {
  const token = localStorage.getItem('access_token')
  axios.put(`http://localhost:8000/task_management/tasks/task_update/${selectedTask.value.id}/`, selectedTask.value, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(() => {
    alert("更新しました")
    isEditing.value = false
    fetchTasks()
    closeModal()
  })
  .catch(err => {
    console.error("更新失敗:", err)
    alert("更新に失敗しました")
  })
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

function advanceStatus() {
  if (!selectedTask.value) return

  let newStatus = ''
  if (selectedTask.value.status === 'not_started') {
    newStatus = 'in_progress'
  } else if (selectedTask.value.status === 'in_progress') {
    newStatus = 'completed'
  } else {
    return // 完了済みなら何もしない（またはリセットしたければ追加可能）
  }

  const token = localStorage.getItem('access_token')
  axios.patch(`http://localhost:8000/task_management/tasks/task_update/${selectedTask.value.id}/`, {
    status: newStatus
  }, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(() => {
    selectedTask.value.status = newStatus
    fetchTasks() // カレンダー更新
  })
  .catch(e => {
    console.error("ステータス更新エラー", e)
  })
}

const nextStatusLabel = computed(() => {
  if (!selectedTask.value) return ''
  switch (selectedTask.value.status) {
    case 'not_started':
      return '進行'
    case 'in_progress':
      return '完了'
    default:
      return '完了済'
  }
})

</script>

<style scoped>
.calendar-container {
  max-width: 800px;
  margin: auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}

.calendar-day {
  text-align: center;
  font-weight: bold;
  padding: 3px 0;
}

.calendar-cell {
  border: 1px solid #ccc;
  padding: 3px 5px;
  min-height: 60px;
  background-color: #f9f9f9;
}

.calendar-cell .date-number {
  font-weight: bold;
  font-size: 1rem;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 3px 0 0 0;
}

.task-item {
  font-size: 10px;
  background-color: #a77bc2;
  color: white;
  margin: 1px 0;
  padding: 1px 3px;
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
.task-item.high-priority {
  background-color: #e74c3c; /* 赤 */
  font-weight: bold;
}

.task-item.completed {
  text-decoration: line-through;
  opacity: 0.7;
}

.modal h3 input.modal-input {
  font-size: 1.2rem;
  padding: 6px;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.modal-select,
.modal-textarea {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.submit-btn {
  background-color: #a77bc2;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #ccc;
  color: #333;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

</style>
