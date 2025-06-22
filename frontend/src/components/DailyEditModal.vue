<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>日次タスクを編集</h3>
      <form @submit.prevent="updateTask">
        <div class="form-group">
          <label for="name">タスク名</label>
          <input id="name" v-model="form.name" required />
        </div>

        <div class="form-group">
          <label for="priority">優先度</label>
          <select id="priority" v-model="form.priority">
            <option value="high">高</option>
            <option value="medium">中</option>
            <option value="low">低</option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">説明</label>
          <textarea id="description" v-model="form.description" rows="3"></textarea>
        </div>

        <div class="buttons">
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
  name: 'DailyEditModal',
  props: {
    task: Object
  },
  data() {
    return {
      form: { ...this.task }
    }
  },
  methods: {
    async updateTask() {
      const token = localStorage.getItem('access_token')
      try {
        const url = `http://localhost:8000/task_management/daily/daily_task/${this.form.id}/`

        await axios.put(url, this.form, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        alert('タスクを更新しました')
        this.$emit('updated')
        this.$emit('close')
        location.reload() // ← ページをリロードする
      } catch (e) {
        console.error('更新エラー:', e)
        alert('更新に失敗しました')
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
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 350px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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

input,
select,
textarea {
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
