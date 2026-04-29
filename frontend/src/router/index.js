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
  
  // ========== 个人主页模块 ==========
  {
    path: '/profile/:id',
    name: 'UserProfile',
    component: () => import('@/views/profile/Profile.vue')
  },
  {
    path: '/profile/edit',
    name: 'EditProfile',
    component: () => import('@/views/profile/EditProfile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my/favorites',
    name: 'MyFavorites',
    component: () => import('@/views/profile/MyFavorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my/followers',
    name: 'MyFollowers',
    component: () => import('@/views/profile/MyFollowers.vue'),
    meta: { requiresAuth: true }
  },
  
  // ========== 求职模块 ==========
  {
    path: '/jobs',
    name: 'JobList',
    component: () => import('@/views/jobs/JobList.vue')
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: () => import('@/views/jobs/JobDetail.vue')
  },
  {
    path: '/resume',
    name: 'Resume',
    component: () => import('@/views/jobs/Resume.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications',
    name: 'MyApplications',
    component: () => import('@/views/jobs/MyApplications.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/interview',
    name: 'InterviewList',
    component: () => import('@/views/jobs/InterviewList.vue')
  },
  {
    path: '/interview/:id',
    name: 'InterviewDetail',
    component: () => import('@/views/jobs/InterviewDetail.vue')
  },
  {
    path: '/campus-talks',
    name: 'CampusTalks',
    component: () => import('@/views/jobs/CampusTalks.vue')
  },
  {
    path: '/campus-talks/:id',
    name: 'CampusTalkDetail',
    component: () => import('@/views/jobs/CampusTalkDetail.vue')
  },
  
  // ========== 培训学习模块 ==========
  {
    path: '/training',
    name: 'Training',
    component: () => import('@/views/training/TrainingHome.vue')
  },
  {
    path: '/training/courses',
    name: 'CourseList',
    component: () => import('@/views/training/CourseList.vue')
  },
  {
    path: '/training/courses/:id',
    name: 'CourseDetail',
    component: () => import('@/views/training/CourseDetail.vue')
  },
  {
    path: '/training/my-courses',
    name: 'MyCourses',
    component: () => import('@/views/training/MyCourses.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/training/materials',
    name: 'MaterialList',
    component: () => import('@/views/training/MaterialList.vue')
  },
  {
    path: '/training/materials/:id',
    name: 'MaterialDetail',
    component: () => import('@/views/training/MaterialDetail.vue')
  },
  {
    path: '/training/my-materials',
    name: 'MyMaterials',
    component: () => import('@/views/training/MyMaterials.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/training/certifications',
    name: 'Certifications',
    component: () => import('@/views/training/Certifications.vue')
  },
  {
    path: '/training/certifications/:id',
    name: 'CertificationDetail',
    component: () => import('@/views/training/CertificationDetail.vue')
  },
  
  // ========== 交友社交模块 ==========
  {
    path: '/social',
    name: 'SocialFeed',
    component: () => import('@/views/social/Feed.vue')
  },
  {
    path: '/social/post/:id',
    name: 'PostDetail',
    component: () => import('@/views/social/PostDetail.vue')
  },
  {
    path: '/social/circles',
    name: 'TopicList',
    component: () => import('@/views/social/TopicList.vue')
  },
  {
    path: '/social/topics/:id',
    name: 'TopicDetail',
    component: () => import('@/views/social/TopicDetail.vue')
  },
  {
    path: '/social/alumni',
    name: 'AlumniCircle',
    component: () => import('@/views/social/AlumniCircle.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/social/events',
    name: 'EventList',
    component: () => import('@/views/social/EventList.vue')
  },
  {
    path: '/social/events/create',
    name: 'CreateEvent',
    component: () => import('@/views/social/CreateEvent.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/social/events/:id',
    name: 'EventDetail',
    component: () => import('@/views/social/EventDetail.vue')
  },
  {
    path: '/social/events/:id/edit',
    name: 'EditEvent',
    component: () => import('@/views/social/CreateEvent.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/social/my-events',
    name: 'MyEvents',
    component: () => import('@/views/social/MyEvents.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('@/views/social/Messages.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/messages/:userId',
    name: 'Chat',
    component: () => import('@/views/social/Chat.vue'),
    meta: { requiresAuth: true }
  },
  
  // ========== 跳蚤市场模块 ==========
  {
    path: '/flea',
    name: 'FleaMarket',
    component: () => import('@/views/flea/FleaMarket.vue')
  },
  {
    path: '/flea/items/:id',
    name: 'ItemDetail',
    component: () => import('@/views/flea/ItemDetail.vue')
  },
  {
    path: '/flea/publish',
    name: 'PublishItem',
    component: () => import('@/views/flea/PublishItem.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/flea/my-items',
    name: 'MyItems',
    component: () => import('@/views/flea/MyItems.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/flea/wanted',
    name: 'WantedList',
    component: () => import('@/views/flea/WantedList.vue')
  },
  
  // ========== 企业端路由 ==========
  {
    path: '/company',
    component: () => import('@/views/company/Layout.vue'),
    meta: { requiresAuth: true, role: 'company_or_admin' },
    children: [
      {
        path: '',
        name: 'CompanyDashboard',
        component: () => import('@/views/company/Dashboard.vue')
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
      },
      {
        path: 'campus-talks',
        name: 'CompanyCampusTalks',
        component: () => import('@/views/company/CampusTalks.vue')
      },
      {
        path: 'courses',
        name: 'CompanyCourses',
        component: () => import('@/views/company/Courses.vue')
      },
      {
        path: 'courses/create',
        name: 'CreateCourse',
        component: () => import('@/views/company/CourseForm.vue')
      },
      {
        path: 'courses/edit/:id',
        name: 'EditCourse',
        component: () => import('@/views/company/CourseForm.vue')
      },
      {
        path: 'certifications',
        name: 'CompanyCertifications',
        component: () => import('@/views/company/Certifications.vue')
      },
      {
        path: 'certifications/create',
        name: 'CreateCertification',
        component: () => import('@/views/company/CertificationForm.vue')
      },
      {
        path: 'certifications/edit/:id',
        name: 'EditCertification',
        component: () => import('@/views/company/CertificationForm.vue')
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
  if (to.meta.role) {
    const userRole = userStore.userInfo?.role
    // company_or_admin 角色：允许 company 或 admin 访问
    if (to.meta.role === 'company_or_admin') {
      if (userRole !== 'company' && userRole !== 'admin') {
        return next('/')
      }
    } else if (userRole !== to.meta.role) {
      return next('/')
    }
  }
  
  // 游客页面（登录后不能访问）
  if (to.meta.guest && userStore.isLoggedIn) {
    // 根据角色跳转到不同页面
    if (userStore.userInfo?.role === 'company') {
      return next('/company')
    } else {
      return next(`/profile/${userStore.userInfo?.id}`)
    }
  }
  
  next()
})

export default router
