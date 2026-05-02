<template>
  <view class="social-page">
    <!-- 顶部导航 -->
    <view class="page-header">
      <view class="header-content">
        <text class="header-title">社交动态</text>
        <text class="header-desc">分享生活，交流经验</text>
      </view>
      <view class="header-actions" v-if="userStore.isLoggedIn">
        <view class="action-btn" @click="goToPublish">
          <text class="action-icon">✏️</text>
        </view>
      </view>
    </view>
    
    <!-- 动态列表 -->
    <scroll-view 
      class="feed-list" 
      scroll-y 
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载中 -->
      <view class="loading-tip" v-if="loading && feedList.length === 0">
        <text>加载中...</text>
      </view>
      
      <!-- 未登录提示 -->
      <view class="login-prompt" v-if="!userStore.isLoggedIn">
        <text class="prompt-icon">💬</text>
        <text class="prompt-title">登录后查看动态</text>
        <text class="prompt-desc">登录后可以发布动态、与校友互动</text>
        <button class="btn-login" @click="goToLogin">立即登录</button>
      </view>
      
      <!-- 空状态 -->
      <view class="empty-state" v-if="!loading && feedList.length === 0 && userStore.isLoggedIn">
        <text class="empty-icon">📝</text>
        <text class="empty-text">暂无动态</text>
        <text class="empty-tip">快来发布第一条动态吧</text>
        <button class="btn-publish" @click="goToPublish">发布动态</button>
      </view>
      
      <!-- 动态列表 -->
      <view class="feed-cards" v-else>
        <view class="feed-card" v-for="item in feedList" :key="item.id">
          <view class="feed-header">
            <view class="user-info">
              <view class="user-avatar">
                <text class="avatar-text">{{ item.author?.username?.charAt(0)?.toUpperCase() || 'U' }}</text>
              </view>
              <view class="user-detail">
                <text class="user-name">{{ item.author?.username || '用户' }}</text>
                <text class="feed-time">{{ formatTime(item.created_at) }}</text>
              </view>
            </view>
          </view>
          
          <view class="feed-content">
            <text class="content-text">{{ item.content }}</text>
          </view>
          
          <view class="feed-footer">
            <view class="action-item" @click="toggleLike(item)">
              <text class="action-icon">{{ item.is_liked ? '❤️' : '🤍' }}</text>
              <text class="action-text">{{ item.like_count || 0 }}</text>
            </view>
            <view class="action-item" @click="goToDetail(item.id)">
              <text class="action-icon">💬</text>
              <text class="action-text">{{ item.comment_count || 0 }}</text>
            </view>
            <view class="action-item">
              <text class="action-icon">↗️</text>
              <text class="action-text">分享</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore">
        <text>加载更多...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && feedList.length > 0">
        <text>没有更多了</text>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 120rpx;"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const feedList = ref([])
const loading = ref(false)
const isRefreshing = ref(false)
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  // 一小时内
  if (diff < 60 * 60 * 1000) {
    const minutes = Math.floor(diff / (60 * 1000))
    if (minutes < 1) return '刚刚'
    return `${minutes}分钟前`
  }
  
  // 一天内
  if (diff < 24 * 60 * 60 * 1000) {
    const hours = Math.floor(diff / (60 * 60 * 1000))
    return `${hours}小时前`
  }
  
  // 一周内
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days}天前`
  }
  
  // 格式化日期
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${year}-${month}-${day}`
}

// 获取动态列表
const fetchFeedList = async () => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    // TODO: 调用真实 API
    // const res = await socialApi.getFeed({ page: page.value, per_page: perPage.value })
    
    // 模拟数据
    const mockData = [
      {
        id: 1,
        author: { username: '张三', id: 1 },
        content: '今天收到了心仪公司的offer！感谢这个平台的帮助，分享一下我的面试经验：\n1. 准备充分，了解公司背景\n2. 多刷算法题\n3. 保持自信！\n祝大家都能找到理想的工作！',
        like_count: 28,
        comment_count: 5,
        is_liked: false,
        created_at: new Date(Date.now() - 3600000).toISOString()
      },
      {
        id: 2,
        author: { username: '李四', id: 2 },
        content: '周末参加了学校的招聘会，收获满满！分享一下现场照片 📸',
        like_count: 15,
        comment_count: 3,
        is_liked: true,
        created_at: new Date(Date.now() - 86400000).toISOString()
      },
      {
        id: 3,
        author: { username: '王五', id: 3 },
        content: '有没有同学一起准备考研？可以互相交流复习经验，共同进步！',
        like_count: 42,
        comment_count: 12,
        is_liked: false,
        created_at: new Date(Date.now() - 172800000).toISOString()
      }
    ]
    
    if (page.value === 1) {
      feedList.value = mockData
    } else {
      feedList.value = [...feedList.value, ...mockData]
    }
    
    hasMore.value = page.value < 3
  } catch (error) {
    console.error('获取动态列表失败:', error)
  } finally {
    loading.value = false
    isRefreshing.value = false
  }
}

// 下拉刷新
const onRefresh = () => {
  isRefreshing.value = true
  page.value = 1
  hasMore.value = true
  fetchFeedList()
}

// 加载更多
const onLoadMore = () => {
  if (!hasMore.value || loading.value) return
  page.value++
  fetchFeedList()
}

// 点赞/取消点赞
const toggleLike = (item) => {
  if (!userStore.isLoggedIn) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    goToLogin()
    return
  }
  
  item.is_liked = !item.is_liked
  if (item.is_liked) {
    item.like_count = (item.like_count || 0) + 1
  } else {
    item.like_count = Math.max(0, (item.like_count || 0) - 1)
  }
}

// 页面跳转
const goToLogin = () => {
  uni.navigateTo({ url: '/pages/login/index' })
}

const goToPublish = () => {
  if (!userStore.isLoggedIn) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    goToLogin()
    return
  }
  uni.showToast({ title: '发布功能开发中', icon: 'none' })
}

const goToDetail = (id) => {
  uni.showToast({ title: '详情功能开发中', icon: 'none' })
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    fetchFeedList()
  }
})
</script>

<style lang="scss" scoped>
.social-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 顶部导航
.page-header {
  background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
  padding: 40rpx 30rpx;
  padding-top: 60rpx;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
  display: block;
  margin-bottom: 8rpx;
}

.header-desc {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
}

.header-actions {
  display: flex;
  gap: 20rpx;
}

.action-btn {
  width: 72rpx;
  height: 72rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.action-icon {
  font-size: 36rpx;
}

// 动态列表
.feed-list {
  flex: 1;
  height: 0;
  padding: 20rpx;
}

// 加载提示
.loading-tip {
  text-align: center;
  padding: 40rpx;
  color: #909399;
  font-size: 28rpx;
}

// 未登录提示
.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 40rpx;
}

.prompt-icon {
  font-size: 120rpx;
  margin-bottom: 24rpx;
}

.prompt-title {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 12rpx;
}

.prompt-desc {
  font-size: 26rpx;
  color: #909399;
  margin-bottom: 40rpx;
}

.btn-login {
  background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
  color: #fff;
  font-size: 28rpx;
  padding: 20rpx 60rpx;
  border-radius: 40rpx;
  border: none;
  
  &::after {
    border: none;
  }
}

// 空状态
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #606266;
  margin-bottom: 12rpx;
}

.empty-tip {
  font-size: 26rpx;
  color: #c0c4cc;
  margin-bottom: 40rpx;
}

.btn-publish {
  background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
  color: #fff;
  font-size: 28rpx;
  padding: 20rpx 60rpx;
  border-radius: 40rpx;
  border: none;
  
  &::after {
    border: none;
  }
}

// 动态卡片
.feed-cards {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.feed-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.feed-header {
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
}

.user-detail {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.feed-time {
  font-size: 22rpx;
  color: #c0c4cc;
}

// 内容
.feed-content {
  margin-bottom: 24rpx;
}

.content-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.8;
  white-space: pre-wrap;
}

// 底部操作
.feed-footer {
  display: flex;
  justify-content: space-around;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 20rpx;
}

.action-icon {
  font-size: 32rpx;
}

.action-text {
  font-size: 24rpx;
  color: #909399;
}

// 加载更多
.load-more {
  text-align: center;
  padding: 30rpx;
  color: #909399;
  font-size: 26rpx;
}

.no-more {
  text-align: center;
  padding: 30rpx;
  color: #c0c4cc;
  font-size: 24rpx;
}
</style>
