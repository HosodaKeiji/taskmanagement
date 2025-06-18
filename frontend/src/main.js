import { createApp } from 'vue'
import App from './App.vue'
import Signup from './components/Signup.vue'
import Login from './components/Login.vue'
import Home from "./components/Home.vue"
import Daily from "./components/Daily.vue"
import Weekly from "./components/Weekly.vue"
import Monthly from "./components/Monthly.vue"
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { path: '/signup', component: Signup },
    { path: '/login', component: Login },
    { path: "/home", component: Home},
    { path: "/daily", component: Daily},
    { path: "/weekly", component: Weekly},
    { path: "/monthly", component: Monthly},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')
