<template>
  <div :class="['sidebar', { closed: isClosed }]">
    <div class="header">
      <h2 class="title">Task <br>Management</h2>
      <button class="toggle-btn" @click="toggleSidebar" aria-label="Toggle Sidebar">
        &#9776;
      </button>
    </div>
    <ul>
      <li><router-link to="/home" exact>ホーム</router-link></li>
      <li><router-link to="/tasks">タスク</router-link></li>
      <li><router-link to="/daily">日次</router-link></li>
      <li><router-link to="/weekly">週次</router-link></li>
      <li><router-link to="/monthly">月次</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SidebarMenu',
  props: ['isClosed'],
  emits: ['toggle'],
  methods: {
    toggleSidebar() {
      this.$emit('toggle')
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: #a77bc2;
  color: white;
  padding: 20px;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  transition: width 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar.closed {
  width: 80px; /* 閉じた時の幅は狭めに */
  padding-left: 10px; /* 余白少し減らす */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0; /* ヘッダーの縮み防止 */
}

.title {
  font-size: 20px;
  margin: 0;
  white-space: nowrap;
  transition: opacity 0.3s ease;
  margin-right: 20px;
}

.sidebar.closed .title {
  opacity: 0;
  pointer-events: none;
  user-select: none;
  width: 0;
  overflow: hidden;
}

.toggle-btn {
  background: transparent;
  border: none;
  font-size: 28px;
  color: white;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  user-select: none;
  flex-shrink: 0; /* ボタンの縮み防止 */
  z-index: 10; /* 必ず手前に */
}

ul {
  list-style: none;
  padding: 0;
  margin-top: 30px;
  flex-grow: 1;
  overflow: hidden;
}

/* 閉じた時はメニュー非表示＆クリック禁止 */
.sidebar.closed ul {
  display: none;
}

li {
  margin: 15px 0;
}

a {
  color: white;
  text-decoration: none;
  display: block;
  padding: 10px 15px;
  border-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
  white-space: nowrap;
}

a:hover {
  background-color: #e6d2f3;
  color: #a77bc2;
}

a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
  background-color: #e6d2f3;
  color: #a77bc2;
}
</style>
