import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/jobs',
    name: 'JobList',
    component: () => import('@/views/JobList.vue')
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: () => import('@/views/JobDetail.vue')
  },
  {
    path: '/resume',
    name: 'Resume',
    component: () => import('@/views/Resume.vue'),
    meta: { requiresAuth: true, role: 'job_seeker' }
  },
  {
    path: '/applications',
    name: 'MyApplications',
    component: () => import('@/views/MyApplications.vue'),
    meta: { requiresAuth: true, role: 'job_seeker' }
  },
  // 企业端路由
  {
    path: '/company',
    component: () => import('@/views/company/Layout.vue'),
    meta: { requiresAuth: true, role: 'company' },
    children: [
      {
        path: '',
        redirect: '/company/jobs'
      },
      {
        path: 'jobs',
        name: 'CompanyJobs',
        component: () => import('@/views/company/Jobs.vue')
      },
      {
        path: 'jobs/create',
        name: 'CreateJob',
        component: () => import('@/views/company/JobForm.vue')
      },
      {
        path: 'jobs/edit/:id',
        name: 'EditJob',
        component: () => import('@/views/company/JobForm.vue')
      },
      {
        path: 'applications',
        name: 'ReceivedApplications',
        component: () => import('@/views/company/Applications.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 初始化用户信息
  await userStore.init()
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return next('/login')
  }
  
  // 需要特定角色的页面
  if (to.meta.role && userStore.userInfo?.role !== to.meta.role) {
    return next('/')
  }
  
  // 游客页面（登录后不能访问）
  if (to.meta.guest && userStore.isLoggedIn) {
    return next('/')
  }
  
  next()
})

export default router
