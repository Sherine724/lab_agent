import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  //要让页面不整个变化跳转，要使用嵌套路由，让左侧的菜单栏保持不动
  routes: [
    { path: '/', redirect: '/manager/home' },
    {
      path: '/manager',
      name: 'Layout',
      component: () => import('@/layouts/Layout.vue'),
      children: [
        { path: 'home', name: 'Home', component: () => import('@/views/Home.vue') },
        { path: 'lib', name: 'Lib', component: () => import('@/views/Lib.vue') },
        { path: 'equ', name: 'Equ', component: () => import('@/views/Equ.vue') },
        { path: 'user', name: 'User', component: () => import('@/views/User.vue') },
        { path: 'profile', name: 'Profile', component: () => import('@/views/Profile.vue') },
        { path: 'password', name: 'Password', component: () => import('@/views/password.vue') }
      ]
    },
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
    { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') }
  ]
})

//全局前置守卫，未登录不允许进入 /manager 下的页面
router.beforeEach((to, from) => {
  const token = getToken()
  //console.log('token:', token)
  if (to.path === '/login' || to.path === '/register') {
    return true
  } else {
    //console.log('当前前往的页面:', to.path)
    return token ? true : '/login'
  }
  //   if (to.path.startsWith('/manager') && !token) {
  //     return '/login'
  //   }
})

export default router
