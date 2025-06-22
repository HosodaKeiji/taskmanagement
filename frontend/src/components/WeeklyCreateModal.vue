<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>週次タスク作成</h3>
      <form @submit.prevent="createTask">
        <label>名前</label>
        <input v-model="task.name" required />

        <label>優先度</label>
        <select v-model="task.priority" required>
          <option value="high">高</option>
          <option value="medium">中</option>
          <option value="low">低</option>
        </select>

        <label>説明</label>
        <textarea v-model="task.description" rows="3" />

        <label>曜日</label>
        <select v-model="task.repeat_rule.day" required>
          <option value="monday">月曜日</option>
          <option value="tuesday">火曜日</option>
          <option value="wednesday">水曜日</option>
          <option value="thursday">木曜日</option>
          <option value="friday">金曜日</option>
          <option value="saturday">土曜日</option>
          <option value="sunday">日曜日</option>
        </select>

        <div class="modal-actions">
          <button type="submit" class="submit-btn">作成</button>
          <button type="button" class="cancel-btn" @click="$emit('close')">キャンセル</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'WeeklyCreateModal',
    data() {
        return {
        task: {
            name: '',
            priority: 'medium',
            description: '',
            type: 'weekly',
            repeat_rule: {
            frequency: 'weekly',
            day: 'monday'  // ← ここを this.task... ではなく文字列で初期化
            }
        },
        error: null
        }
    },
    methods: {
        async createTask() {
        try {
            const token = localStorage.getItem('access_token')
            const payload = {
            ...this.task,
            repeat_rule: {
                frequency: 'weekly',
                day: this.task.repeat_rule.day  // ← ここを day にする（days にしない）
            }
            }
            await axios.post('http://localhost:8000/task_management/weekly/weekly_task/', payload, {
            headers: {
                Authorization: `Bearer ${token}`
            }
            })
            alert('週次タスクを作成しました')
            this.$emit('created')
            this.$emit('close')
        } catch (e) {
            if (e.response && e.response.data) {
            console.error('作成エラー詳細:', e.response.data)
            alert('作成に失敗しました: ' + JSON.stringify(e.response.data))
            } else {
            console.error('作成エラー:', e)
            alert('作成に失敗しました')
            }
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

.error {
  color: red;
  margin-top: 12px;
  text-align: center;
  font-weight: bold;
}
</style>
