<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>タスクを作成</h3>
      <form @submit.prevent="createTask">
        <!-- 基本情報 -->
        <div class="form-group">
          <label for="name">タスク名</label>
          <input id="name" v-model="form.name" required />
        </div>

        <div class="form-group">
          <label for="type">種類</label>
          <select id="type" v-model="form.type">
            <option value="normal">通常</option>
            <option value="daily">日次</option>
            <option value="weekly">週次</option>
            <option value="monthly">月次</option>
          </select>
        </div>

        <div v-if="form.type === 'weekly'" class="form-group">
          <label for="repeat_day">繰り返し曜日</label>
          <select id="repeat_day" v-model="form.repeat_rule.day">
            <option disabled value="">選択してください</option>
            <option value="monday">月</option>
            <option value="tuesday">火</option>
            <option value="wednesday">水</option>
            <option value="thursday">木</option>
            <option value="friday">金</option>
            <option value="saturday">土</option>
            <option value="sunday">日</option>
          </select>
        </div>

        <div v-if="form.type === 'monthly'" class="form-group">
          <label for="repeat_day">繰り返し日（1〜31日）</label>
          <input type="number" min="1" max="31" v-model.number="form.repeat_rule.day" />
        </div>

        <div class="form-group" v-if="form.type === 'normal'">
          <label for="deadline">締切日</label>
          <input id="deadline" type="date" v-model="form.deadline" required />
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
          <label for="status">ステータス</label>
          <select id="status" v-model="form.status">
            <option value="not_started">未着手</option>
            <option value="in_progress">進行中</option>
            <option value="completed">完了</option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">説明</label>
          <textarea id="description" v-model="form.description" rows="3" />
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
  data() {
    return {
      form: {
        name: '',
        type: 'normal',
        deadline: '',
        priority: 'medium',
        status: 'not_started',
        description: '',
        repeat_rule: { frequency: '', day: '' }
      }
    }
  },
  watch: {
    'form.type'(newType) {
      if (newType === 'weekly') {
        this.form.repeat_rule = { frequency: 'weekly', day: '' }
      } else if (newType === 'monthly') {
        this.form.repeat_rule = { frequency: 'monthly', day: '' }
      } else if (newType === 'daily') {
        this.form.repeat_rule = { frequency: 'daily' }
      } else {
        this.form.repeat_rule = null
      }
    }
  },
  methods: {
    async createTask() {
      const token = localStorage.getItem('access_token')
      try {
        const payload = {
          name: this.form.name,
          type: this.form.type,
          deadline: this.form.type === 'normal' ? this.form.deadline : null,
          priority: this.form.priority,
          status: this.form.status,
          description: this.form.description,
          repeat_rule: this.form.repeat_rule || null,
        }
        await axios.post('http://localhost:8000/task_management/tasks/task_create/', payload, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        alert('タスクを作成しました')
        this.$emit('success')
        this.$emit('close')
        location.reload() // ← ページをリロードする
      } catch (e) {
        alert('作成に失敗しました')
        if (e.response && e.response.data) {
          console.error('サーバーエラー:', e.response.data);
        } else {
          console.error(e);
        }
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
