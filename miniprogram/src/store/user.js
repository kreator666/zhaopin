import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(uni.getStorageSync('token') || '')
  const userInfo = ref(null)
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const userRole = computed(() => userInfo.value?.role || '')
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isCompany = computed(() => userInfo.value?.role === 'company')
  const isStudent = computed(() => userInfo.value?.role === 'student')
  const isAlumni = computed(() => userInfo.value?.role === 'alumni')
  
  // 初始化用户状态
  const init = async () => {
    const savedToken = uni.getStorageSync('token')
    if (savedToken) {
      token.value = savedToken
      // 尝试获取用户信息
      try {
        const res = await authApi.getCurrentUser()
        userInfo.value = res.data || res
      } catch (error) {
        console.log('获取用户信息失败，可能token已过期')
        // token 可能过期，清除
        logout()
      }
    }
  }
  
  // 设置 token
  const setToken = (newToken) => {
    token.value = newToken
    uni.setStorageSync('token', newToken)
  }
  
  // 设置用户信息
  const setUserInfo = (info) => {
    userInfo.value = info
    uni.setStorageSync('userInfo', JSON.stringify(info))
  }
  
  // 登录
  const login = async (loginForm) => {
    const res = await authApi.login(loginForm)
    const { access_token, user } = res.data || res
    setToken(access_token)
    setUserInfo(user)
    return user
  }
  
  // 注册
  const register = async (registerForm) => {
    const res = await authApi.register(registerForm)
    return res.data || res
  }
  
  // 退出登录
  const logout = () => {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('userInfo')
  }
  
  // 刷新用户信息
  const refreshUserInfo = async () => {
    if (!token.value) return
    
    try {
      const res = await authApi.getCurrentUser()
      userInfo.value = res.data || res
      uni.setStorageSync('userInfo', JSON.stringify(userInfo.value))
    } catch (error) {
      console.error('刷新用户信息失败:', error)
    }
  }
  
  return {
    // 状态
    token,
    userInfo,
    // 计算属性
    isLoggedIn,
    userRole,
    isAdmin,
    isCompany,
    isStudent,
    isAlumni,
    // 方法
    init,
    setToken,
    setUserInfo,
    login,
    register,
    logout,
    refreshUserInfo
  }
})
