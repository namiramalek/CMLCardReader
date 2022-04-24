import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Index'
import BusinessCard from '../views/BusinessCard'
Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/business-card/:id',
        name: 'BusinessCard',
        component: BusinessCard,
    }

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router