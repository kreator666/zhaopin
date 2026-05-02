<template>
  <view class="register-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">‹</text>
      </view>
      <text class="nav-title">注册账号</text>
      <view class="nav-right"></view>
    </view>
    
    <!-- 注册表单 -->
    <scroll-view class="register-content" scroll-y>
      <!-- 角色选择 -->
      <view class="role-section">
        <view class="section-title">我是</view>
        <view class="role-grid">
          <view 
            class="role-item" 
            :class="{ 'role-active': selectedRole === 'student' }"
            @click="selectRole('student')"
          >
            <text class="role-icon" :class="{ 'icon-active': selectedRole === 'student' }">🎓</text>
            <text class="role-name">学生</text>
            <text class="role-desc">找工作、学习课程</text>
          </view>
          
          <view 
            class="role-item" 
            :class="{ 'role-active': selectedRole === 'alumni' }"
            @click="selectRole('alumni')"
          >
            <text class="role-icon" :class="{ 'icon-active': selectedRole === 'alumni' }">🏆</text>
            <text class="role-name">校友</text>
            <text class="role-desc">已毕业校友</text>
          </view>
          
          <view 
            class="role-item" 
            :class="{ 'role-active': selectedRole === 'company' }"
            @click="selectRole('company')"
          >
            <text class="role-icon" :class="{ 'icon-active': selectedRole === 'company' }">💼</text>
            <text class="role-name">企业</text>
            <text class="role-desc">发布职位招聘</text>
          </view>
        </view>
      </view>
      
      <!-- 表单区域 -->
      <view class="form-section">
        <!-- 基础信息 -->
        <view class="form-group">
          <view class="form-group-title">基础信息</view>
          
          <view class="form-item">
            <text class="form-label">用户名</text>
            <view class="input-wrapper">
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
            <text class="form-label">邮箱</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.email" 
                placeholder="请输入邮箱地址"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">密码</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="password" 
                v-model="form.password" 
                placeholder="请输入密码（至少6位）"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">确认密码</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="password" 
                v-model="form.confirmPassword" 
                placeholder="请再次输入密码"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
        </view>
        
        <!-- 个人信息（学生/校友） -->
        <view class="form-group" v-if="selectedRole === 'student' || selectedRole === 'alumni'">
          <view class="form-group-title">个人信息</view>
          
          <view class="form-item">
            <text class="form-label">真实姓名</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.realName" 
                placeholder="请输入真实姓名"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">手机号</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="number" 
                v-model="form.phone" 
                placeholder="请输入手机号"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item" v-if="selectedRole === 'student'">
            <text class="form-label">学校</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.school" 
                placeholder="请输入学校名称"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item" v-if="selectedRole === 'student'">
            <text class="form-label">专业</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.major" 
                placeholder="请输入专业名称"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
        </view>
        
        <!-- 企业信息 -->
        <view class="form-group" v-if="selectedRole === 'company'">
          <view class="form-group-title">企业信息</view>
          
          <view class="form-item">
            <text class="form-label">公司名称</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.companyName" 
                placeholder="请输入公司全称"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">联系人</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.contactName" 
                placeholder="请输入联系人姓名"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">联系电话</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="number" 
                v-model="form.contactPhone" 
                placeholder="请输入联系电话"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">公司地址</text>
            <view class="input-wrapper">
              <input 
                class="input-field" 
                type="text" 
                v-model="form.companyAddress" 
                placeholder="请输入公司地址"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">公司简介</text>
            <view class="input-wrapper textarea">
              <textarea 
                class="input-field" 
                v-model="form.companyDescription" 
                placeholder="请输入公司简介（选填）"
                placeholder-class="input-placeholder"
              />
            </view>
          </view>
        </view>
      </view>
      
      <!-- 错误提示 -->
      <view class="form-tip" v-if="errorMsg">
        <text class="tip-text">{{ errorMsg }}</text>
      </view>
      
      <!-- 注册按钮 -->
      <view class="form-actions">
        <button 
          class="btn-register" 
          :class="{ 'btn-disabled': loading }"
          :disabled="loading"
          @click="handleRegister"
        >
          <text v-if="loading">注册中...</text>
          <text v-else>注 册</text>
        </button>
      </view>
      
      <!-- 底部提示 -->
      <view class="footer-tip">
        <text class="tip-text">已有账号？</text>
        <text class="link-text" @click="goToLogin">立即登录</text>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 60rpx;"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/store/user'
import authApi from '@/api/auth'

const userStore = useUserStore()

const selectedRole = ref('student')
const loading = ref(false)
const errorMsg = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  // 学生/校友
  realName: '',
  phone: '',
  school: '',
  major: '',
  // 企业
  companyName: '',
  contactName: '',
  contactPhone: '',
  companyAddress: '',
  companyDescription: ''
})

// 选择角色
const selectRole = (role) => {
  selectedRole.value = role
}

// 返回
const goBack = () => {
  uni.navigateBack()
}

// 去登录
const goToLogin = () => {
  uni.navigateTo({ url: '/pages/login/index' })
}

// 注册
const handleRegister = async () => {
  // 基础验证
  if (!form.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  if (!form.email.trim()) {
    errorMsg.value = '请输入邮箱'
    return
  }
  if (!form.password) {
    errorMsg.value = '请输入密码'
    return
  }
  if (form.password.length < 6) {
    errorMsg.value = '密码长度不能少于6位'
    return
  }
  if (form.password !== form.confirmPassword) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }
  
  // 构建注册数据
  const registerData = {
    username: form.username.trim(),
    email: form.email.trim(),
    password: form.password,
    role: selectedRole.value,
    profile: {}
  }
  
  // 学生/校友
  if (selectedRole.value === 'student' || selectedRole.value === 'alumni') {
    if (form.realName) registerData.profile.real_name = form.realName
    if (form.phone) registerData.profile.phone = form.phone
    if (form.school) registerData.profile.school = form.school
    if (form.major) registerData.profile.major = form.major
  }
  
  // 企业
  if (selectedRole.value === 'company') {
    if (form.companyName) registerData.profile.company_name = form.companyName
    if (form.contactName) registerData.profile.contact_name = form.contactName
    if (form.contactPhone) registerData.profile.contact_phone = form.contactPhone
    if (form.companyAddress) registerData.profile.company_address = form.companyAddress
    if (form.companyDescription) registerData.profile.company_description = form.companyDescription
  }
  
  errorMsg.value = ''
  loading.value = true
  
  try {
    const res = await userStore.register(registerData)
    
    uni.showToast({
      title: '注册成功',
      icon: 'success'
    })
    
    // 自动登录
    try {
      await userStore.login({
        username: form.username.trim(),
        password: form.password
      })
      
      setTimeout(() => {
        uni.switchTab({ url: '/pages/index/index' })
      }, 1500)
    } catch (loginErr) {
      // 登录失败，跳转登录页
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/index' })
      }, 1500)
    }
  } catch (error) {
    const errMsg = error?.error || error?.response?.data?.error || '注册失败，请重试'
    errorMsg.value = errMsg
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 导航栏
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 30rpx;
  padding-top: 40rpx;
  background-color: #fff;
  border-bottom: 1rpx solid #f0f0f0;
}

.nav-back {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-icon {
  font-size: 48rpx;
  color: #333;
  font-weight: bold;
}

.nav-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.nav-right {
  width: 60rpx;
}

// 滚动内容
.register-content {
  flex: 1;
  height: 0;
}

// 角色选择
.role-section {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.role-grid {
  display: flex;
  gap: 20rpx;
}

.role-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30rpx 20rpx;
  background-color: #f5f7fa;
  border-radius: 16rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
  
  &.role-active {
    background-color: #ecf5ff;
    border-color: #409eff;
  }
}

.role-icon {
  font-size: 48rpx;
  margin-bottom: 12rpx;
  opacity: 0.6;
  
  &.icon-active {
    opacity: 1;
  }
}

.role-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.role-desc {
  font-size: 22rpx;
  color: #909399;
}

// 表单区域
.form-section {
  background-color: #fff;
  padding: 0 30rpx;
  margin-bottom: 20rpx;
}

.form-group {
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
}

.form-group-title {
  font-size: 26rpx;
  font-weight: bold;
  color: #606266;
  margin-bottom: 24rpx;
}

.form-item {
  margin-bottom: 24rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.form-label {
  display: block;
  font-size: 28rpx;
  color: #606266;
  margin-bottom: 12rpx;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 12rpx;
  padding: 24rpx 28rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
  
  &:focus-within {
    border-color: #409eff;
    background-color: #fff;
  }
  
  &.textarea {
    min-height: 160rpx;
    align-items: flex-start;
  }
}

.input-field {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.input-placeholder {
  color: #c0c4cc;
}

// 错误提示
.form-tip {
  margin: 20rpx 30rpx;
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
  padding: 0 30rpx;
  margin-top: 30rpx;
}

.btn-register {
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

// 底部提示
.footer-tip {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40rpx 30rpx;
}

.tip-text {
  font-size: 26rpx;
  color: #909399;
}

.link-text {
  font-size: 26rpx;
  color: #409eff;
  margin-left: 8rpx;
}
</style>
