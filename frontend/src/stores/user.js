import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  const loading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isCompany = computed(() => userInfo.value?.role === 'company')
  // 学生/求职者/校友都属于个人用户（非企业）
  const isPersonalUser = computed(() => !isCompany.value)
  // 兼容旧代码：job_seeker 或 student 都视为求职者
  const isJobSeeker = computed(() => ['job_seeker', 'student', 'alumni'].includes(userInfo.value?.role))

  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
  }

  const fetchUserInfo = async () => {
    if (!token.value) return
    try {
      loading.value = true
      const res = await authApi.getCurrentUser()
      userInfo.value = res
      return res
    } catch (error) {
      logout()
      throw error
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  // 初始化时如果有token，自动获取用户信息
  const init = async () => {
    if (token.value && !userInfo.value) {
      await fetchUserInfo()
    }
  }

  return {
    token,
    userInfo,
    loading,
    isLoggedIn,
    isJobSeeker,
    isCompany,
    isPersonalUser,
    setToken,
    setUserInfo,
    fetchUserInfo,
    logout,
    init
  }
})
