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
  const isJobSeeker = computed(() => userInfo.value?.role === 'job_seeker')
  const isCompany = computed(() => userInfo.value?.role === 'company')

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
    setToken,
    setUserInfo,
    fetchUserInfo,
    logout,
    init
  }
})
