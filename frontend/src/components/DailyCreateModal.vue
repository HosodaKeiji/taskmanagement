<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>日次タスクを作成</h3>
      <form @submit.prevent="createTask">
        <div class="form-group">
          <label>タスク名</label>
          <input v-model="form.name" required />

          <label>優先度</label>
          <select v-model="form.priority">
            <option value="high">高</option>
            <option value="medium">中</option>
            <option value="low">低</option>
          </select>

          <label>説明</label>
          <textarea v-model="form.description" rows="3" />
        </div>

        <div class="buttons">
          <button type="submit" class="submit-btn">作成</button>
          <button type="button" class="cancel-btn" @click="$emit('close')">閉じる</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DailyCreateModal',
  data() {
    return {
      form: {
        name: '',
        priority: 'medium',
        description: '',
        status: 'not_started',
        type: 'daily',
        repeat_rule: { frequency: 'daily' }
      }
    }
  },
  methods: {
    async createTask() {
      const token = localStorage.getItem('access_token')
      try {
        await axios.post('http://localhost:8000/task_management/daily/daily_task/', this.form, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        alert('日次タスクを作成しました')
        this.$emit('created')
        this.$emit('close')
      } catch (e) {
        console.error('作成エラー:', e)
        alert('作成に失敗しました')
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  width: 340px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

h3 {
  margin-bottom: 16px;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}

label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #555;
}

input, select, textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

textarea {
  resize: vertical;
}

.buttons {
  margin-top: 20px;
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

