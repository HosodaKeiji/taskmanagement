import { createApp } from 'vue'
import App from './App.vue'
import Signup from './components/Signup.vue'
import Login from './components/Login.vue'
import Home from "./components/Home.vue"
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { path: '/signup', component: Signup },
    { path: '/login', component: Login },
    { path: "/home", component: Home},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')
