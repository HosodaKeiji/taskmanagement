<template>
  <div id="app">
    <!-- ログイン・サインアップページではサイドバーを非表示 -->
    <SidebarMenu
      v-if="!hideSidebar"
      :isClosed="isSidebarClosed"
      @toggle="toggleSidebar"
    />
    <div :class="['main-content', {
      closed: isSidebarClosed && !hideSidebar,
      'no-sidebar': hideSidebar
    }]">
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
  computed: {
    hideSidebar() {
      const path = this.$route.path
      return path === '/login' || path === '/signup'
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

.main-content.no-sidebar {
  margin-left: 0;
}

</style>
