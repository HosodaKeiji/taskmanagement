<template>
  <div id="app">
    <SidebarMenu :isClosed="isSidebarClosed" @toggle="toggleSidebar" />
    <div :class="['main-content', { closed: isSidebarClosed }]">
      <router-view />
    </div>
  </div>
</template>

<script>
import SidebarMenu from './components/Sidebar.vue'

export default {
  components: { SidebarMenu },
  data() {
    return {
      isSidebarClosed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarClosed = !this.isSidebarClosed
    }
  }
}
</script>

<style>
.main-content {
  margin-left: 200px; /* サイドバー開いてるとき */
  padding: 20px;
  transition: margin-left 0.3s ease;
}

.main-content.closed {
  margin-left: 80px; /* サイドバー閉じてるときは余白なし */
}

</style>
