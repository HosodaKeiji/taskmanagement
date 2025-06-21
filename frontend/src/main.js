import { createApp } from 'vue'
import App from './App.vue'
import Signup from './views/Signup.vue'
import Login from './views/Login.vue'
import Home from "./views/Home.vue"
import Daily from "./views/Daily.vue"
import Weekly from "./views/Weekly.vue"
import Monthly from "./views/Monthly.vue"
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
