<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>月次タスク編集</h3>
      <button class="delete-icon" @click="deleteTask" title="削除">🗑️</button>
      <form @submit.prevent="updateTask">
        <label>名前</label>
        <input v-model="editedTask.name" required />

        <label>優先度</label>
        <select v-model="editedTask.priority" required>
          <option value="high">高</option>
          <option value="medium">中</option>
          <option value="low">低</option>
        </select>

        <label>説明</label>
        <textarea v-model="editedTask.description" rows="3" />

        <label>繰り返し日（1〜31日）</label>
        <select v-model="editedTask.repeat_rule.day" required>
        <option v-for="n in 31" :key="n" :value="n">{{ n }}日</option>
        </select>

        <div class="modal-actions">
          <button type="submit" class="submit-btn">保存</button>
          <button type="button" class="cancel-btn" @click="$emit('close')">閉じる</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MonthlyEditModal',
  props: ['task'],
  data() {
    return {
      editedTask: JSON.parse(JSON.stringify(this.task))
    }
  },
  methods: {
    async updateTask() {
      try {
        const token = localStorage.getItem('access_token')
        await axios.put(`http://localhost:8000/task_management/monthly/monthly_task/${this.editedTask.id}/`, this.editedTask, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        alert('月次タスクを更新しました')
        this.$emit('updated')
        this.$emit('close')
      } catch (e) {
        console.error('更新エラー:', e)
        alert('更新に失敗しました')
      }
    },

    async deleteTask() {
      if (!confirm('このタスクを削除してもよろしいですか？')) return

      const token = localStorage.getItem('access_token')
      try {
        const url = `http://localhost:8000/task_management/tasks/task/${this.editedTask.id}/delete/`
        await axios.delete(url, {
          headers: { Authorization: `Bearer ${token}` }
        })

        alert('削除しました')
        this.$emit('deleted')
        this.$emit('close')
        location.reload()
      } catch (err) {
        console.error('削除失敗:', err)
        alert('削除に失敗しました')
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 340px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal h3 {
  margin-bottom: 16px;
  color: #a77bc2;
  text-align: center;
}

label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #555;
}

input,
select,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.submit-btn {
  background-color: #a77bc2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #935bb3;
}

.cancel-btn {
  background-color: #ccc;
  color: #333;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-btn:hover {
  background-color: #999;
}

.delete-icon {
  position: absolute;
  top: 16px;
  right: 16px;
  background-color: transparent;
  border: none;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.delete-icon:hover {
  color: #e74c3c;
}
</style>
