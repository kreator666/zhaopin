<template>
  <view class="login-page">
    <!-- 顶部装饰 -->
    <view class="login-header">
      <view class="logo-section">
        <view class="logo-icon">
          <text class="logo-text">🎯</text>
        </view>
        <text class="app-name">求职社交平台</text>
        <text class="app-slogan">求职+社交，助力职业成长</text>
      </view>
    </view>
    
    <!-- 登录表单 -->
    <view class="login-content">
      <view class="form-section">
        <view class="form-title">账号登录</view>
        
        <view class="form-item">
          <view class="input-wrapper">
            <text class="input-icon">👤</text>
            <input 
              class="input-field" 
              type="text" 
              v-model="form.username" 
              placeholder="请输入用户名"
              placeholder-class="input-placeholder"
            />
          </view>
        </view>
        
        <view class="form-item">
          <view class="input-wrapper">
            <text class="input-icon">🔒</text>
            <input 
              class="input-field" 
              type="password" 
              v-model="form.password" 
              placeholder="请输入密码"
              placeholder-class="input-placeholder"
              @confirm="handleLogin"
            />
          </view>
        </view>
        
        <view class="form-tip" v-if="errorMsg">
          <text class="tip-text">{{ errorMsg }}</text>
        </view>
        
        <view class="form-actions">
          <button 
            class="btn-login" 
            :class="{ 'btn-disabled': loading }"
            :disabled="loading"
            @click="handleLogin"
          >
            <text v-if="loading">登录中...</text>
            <text v-else>登 录</text>
          </button>
        </view>
        
        <view class="other-actions">
          <view class="action-item" @click="goToRegister">
            <text class="action-text">没有账号？去注册</text>
          </view>
          <view class="action-item" @click="goToHome">
            <text class="action-text">随便看看</text>
          </view>
        </view>
      </view>
      
      <!-- 分隔线 -->
      <view class="divider-section">
        <view class="divider-line"></view>
        <text class="divider-text">快速登录</text>
        <view class="divider-line"></view>
      </view>
      
      <!-- 第三方登录（预留） -->
      <view class="third-party-section">
        <view class="third-party-item" @click="wxLogin">
          <view class="third-party-icon wechat">
            <text class="icon-text">💬</text>
          </view>
          <text class="third-party-text">微信登录</text>
        </view>
      </view>
    </view>
    
    <!-- 底部版权 -->
    <view class="login-footer">
      <text class="copyright-text">© 2024 求职社交平台</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const errorMsg = ref('')

// 登录
const handleLogin = async () => {
  if (!form.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  if (!form.password) {
    errorMsg.value = '请输入密码'
    return
  }
  
  errorMsg.value = ''
  loading.value = true
  
  try {
    await userStore.login({
      username: form.username.trim(),
      password: form.password
    })
    
    uni.showToast({
      title: '登录成功',
      icon: 'success'
    })
    
    setTimeout(() => {
      // 根据角色跳转
      if (userStore.isAdmin.value) {
        uni.showToast({
          title: '请使用运营端登录',
          icon: 'none'
        })
        return
      }
      uni.switchTab({ url: '/pages/index/index' })
    }, 1500)
  } catch (error) {
    const errMsg = error?.error || error?.response?.data?.error || '登录失败，请检查用户名和密码'
    errorMsg.value = errMsg
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}

// 微信登录（预留）
const wxLogin = () => {
  uni.showToast({
    title: '微信登录功能开发中',
    icon: 'none'
  })
}

// 跳转注册
const goToRegister = () => {
  uni.navigateTo({ url: '/pages/register/index' })
}

// 随便看看
const goToHome = () => {
  uni.switchTab({ url: '/pages/index/index' })
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #409eff 0%, #67c23a 100%);
  display: flex;
  flex-direction: column;
}

// 顶部
.login-header {
  padding: 80rpx 0 60rpx;
  display: flex;
  justify-content: center;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 160rpx;
  height: 160rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24rpx;
}

.logo-text {
  font-size: 80rpx;
}

.app-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 12rpx;
}

.app-slogan {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
}

// 表单区域
.login-content {
  flex: 1;
  background-color: #fff;
  border-radius: 40rpx 40rpx 0 0;
  padding: 60rpx 40rpx;
}

.form-section {
  margin-bottom: 50rpx;
}

.form-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 50rpx;
  text-align: center;
}

.form-item {
  margin-bottom: 30rpx;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 12rpx;
  padding: 28rpx 30rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
  
  &:focus-within {
    border-color: #409eff;
    background-color: #fff;
  }
}

.input-icon {
  font-size: 32rpx;
  margin-right: 20rpx;
}

.input-field {
  flex: 1;
  font-size: 30rpx;
  color: #333;
}

.input-placeholder {
  color: #c0c4cc;
}

// 错误提示
.form-tip {
  margin-bottom: 30rpx;
  padding: 16rpx 20rpx;
  background-color: #fef0f0;
  border-radius: 8rpx;
}

.tip-text {
  font-size: 24rpx;
  color: #f56c6c;
}

// 按钮
.form-actions {
  margin-top: 40rpx;
}

.btn-login {
  width: 100%;
  height: 96rpx;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: #fff;
  border-radius: 48rpx;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.btn-disabled {
    opacity: 0.7;
  }
  
  &::after {
    border: none;
  }
}

// 其他操作
.other-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30rpx;
  padding: 0 10rpx;
}

.action-text {
  font-size: 26rpx;
  color: #409eff;
}

// 分隔线
.divider-section {
  display: flex;
  align-items: center;
  margin-bottom: 50rpx;
}

.divider-line {
  flex: 1;
  height: 1rpx;
  background-color: #e4e7ed;
}

.divider-text {
  padding: 0 30rpx;
  font-size: 24rpx;
  color: #c0c4cc;
}

// 第三方登录
.third-party-section {
  display: flex;
  justify-content: center;
}

.third-party-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.third-party-icon {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12rpx;
}

.wechat {
  background-color: #07c160;
}

.icon-text {
  font-size: 48rpx;
}

.third-party-text {
  font-size: 24rpx;
  color: #606266;
}

// 底部
.login-footer {
  padding: 30rpx;
  background-color: #fff;
  text-align: center;
}

.copyright-text {
  font-size: 22rpx;
  color: #c0c4cc;
}
</style>
