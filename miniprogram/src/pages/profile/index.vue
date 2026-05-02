<template>
  <view class="profile-page">
    <!-- 顶部用户信息 -->
    <view class="profile-header" v-if="userStore.isLoggedIn">
      <view class="user-info">
        <view class="user-avatar">
          <text class="avatar-text">{{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</text>
        </view>
        <view class="user-detail">
          <text class="user-name">{{ userStore.userInfo?.username || '用户' }}</text>
          <text class="user-role">{{ getRoleName(userStore.userInfo?.role) }}</text>
        </view>
        <view class="edit-btn" @click="goToEditProfile">
          <text class="edit-icon">✏️</text>
        </view>
      </view>
      
      <!-- 数据统计 -->
      <view class="stats-section">
        <view class="stat-item" @click="goToMyCourses">
          <text class="stat-value">{{ stats.courseCount }}</text>
          <text class="stat-label">我的课程</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item" @click="goToFavorites">
          <text class="stat-value">{{ stats.favoriteCount }}</text>
          <text class="stat-label">我的收藏</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item" @click="goToFollowers">
          <text class="stat-value">{{ stats.followerCount }}</text>
          <text class="stat-label">我的粉丝</text>
        </view>
      </view>
    </view>
    
    <!-- 未登录状态 -->
    <view class="login-prompt" v-else @click="goToLogin">
      <view class="prompt-avatar">
        <text class="prompt-icon">👤</text>
      </view>
      <text class="prompt-text">点击登录</text>
    </view>
    
    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-group">
        <view class="menu-item" @click="goToMyCourses" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">📚</text>
            <text class="menu-text">我的课程</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToMyMaterials" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">📄</text>
            <text class="menu-text">我的学习资料</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToMyFleaItems" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">🏪</text>
            <text class="menu-text">我的发布</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToMyApplications" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">📋</text>
            <text class="menu-text">我的投递</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>
      
      <view class="menu-group">
        <view class="menu-item" @click="goToFavorites" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">❤️</text>
            <text class="menu-text">我的收藏</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToFollowers" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">👥</text>
            <text class="menu-text">我的粉丝</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToMessages" v-if="userStore.isLoggedIn">
          <view class="menu-left">
            <text class="menu-icon">💬</text>
            <text class="menu-text">我的消息</text>
          </view>
          <view class="menu-badge" v-if="unreadCount > 0">{{ unreadCount }}</view>
          <text class="menu-arrow">›</text>
        </view>
      </view>
      
      <view class="menu-group">
        <view class="menu-item" @click="goToAbout">
          <view class="menu-left">
            <text class="menu-icon">ℹ️</text>
            <text class="menu-text">关于我们</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="goToSettings">
          <view class="menu-left">
            <text class="menu-icon">⚙️</text>
            <text class="menu-text">设置</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>
      
      <!-- 退出登录 -->
      <view class="logout-section" v-if="userStore.isLoggedIn">
        <button class="btn-logout" @click="handleLogout">退出登录</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const stats = ref({
  courseCount: 0,
  favoriteCount: 0,
  followerCount: 0
})

const unreadCount = ref(0)

// 角色名称映射
const roleMap = {
  student: '学生',
  alumni: '校友',
  company: '企业用户',
  admin: '管理员'
}

const getRoleName = (role) => {
  return roleMap[role] || '用户'
}

// 页面跳转
const goToLogin = () => {
  uni.navigateTo({ url: '/pages/login/index' })
}

const goToEditProfile = () => {
  uni.showToast({ title: '编辑个人资料功能开发中', icon: 'none' })
}

const goToMyCourses = () => {
  uni.navigateTo({ url: '/pages/training/my-courses' })
}

const goToMyMaterials = () => {
  uni.showToast({ title: '我的学习资料功能开发中', icon: 'none' })
}

const goToMyFleaItems = () => {
  uni.navigateTo({ url: '/pages/flea/my-items' })
}

const goToMyApplications = () => {
  uni.showToast({ title: '我的投递功能开发中', icon: 'none' })
}

const goToFavorites = () => {
  uni.showToast({ title: '我的收藏功能开发中', icon: 'none' })
}

const goToFollowers = () => {
  uni.showToast({ title: '我的粉丝功能开发中', icon: 'none' })
}

const goToMessages = () => {
  uni.navigateTo({ url: '/pages/social/messages' })
}

const goToAbout = () => {
  uni.showToast({ title: '关于我们功能开发中', icon: 'none' })
}

const goToSettings = () => {
  uni.showToast({ title: '设置功能开发中', icon: 'none' })
}

// 退出登录
const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.showToast({
          title: '已退出登录',
          icon: 'success'
        })
      }
    }
  })
}

// 获取数据
const fetchStats = () => {
  // TODO: 调用API获取真实数据
  stats.value = {
    courseCount: 2,
    favoriteCount: 10,
    followerCount: 5
  }
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    fetchStats()
  }
})
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 120rpx;
}

// 头部
.profile-header {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 40rpx 30rpx;
  padding-top: 60rpx;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 40rpx;
}

.user-avatar {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.avatar-text {
  font-size: 48rpx;
  font-weight: bold;
  color: #409eff;
}

.user-detail {
  flex: 1;
  margin-left: 24rpx;
}

.user-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8rpx;
  display: block;
}

.user-role {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  background-color: rgba(255, 255, 255, 0.2);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
}

.edit-btn {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-icon {
  font-size: 32rpx;
}

// 统计数据
.stats-section {
  display: flex;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 16rpx;
  padding: 24rpx 0;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.stat-divider {
  width: 1rpx;
  background-color: rgba(255, 255, 255, 0.3);
}

// 未登录提示
.login-prompt {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 60rpx 30rpx;
  padding-top: 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.prompt-avatar {
  width: 160rpx;
  height: 160rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24rpx;
}

.prompt-icon {
  font-size: 80rpx;
}

.prompt-text {
  font-size: 28rpx;
  color: #fff;
}

// 菜单区域
.menu-section {
  margin-top: 20rpx;
}

.menu-group {
  background-color: #fff;
  margin-bottom: 20rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:active {
    background-color: #f5f7fa;
  }
}

.menu-left {
  display: flex;
  align-items: center;
}

.menu-icon {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.menu-text {
  font-size: 30rpx;
  color: #333;
}

.menu-arrow {
  font-size: 32rpx;
  color: #c0c4cc;
}

.menu-badge {
  background-color: #f56c6c;
  color: #fff;
  font-size: 22rpx;
  padding: 2rpx 12rpx;
  border-radius: 20rpx;
  margin-right: 12rpx;
}

// 退出登录
.logout-section {
  padding: 40rpx 30rpx;
}

.btn-logout {
  width: 100%;
  height: 90rpx;
  background-color: #fff;
  color: #f56c6c;
  border-radius: 12rpx;
  font-size: 30rpx;
  border: none;
  
  &::after {
    border: none;
  }
}
</style>
