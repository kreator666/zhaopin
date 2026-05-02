<template>
  <view class="certifications-page">
    <!-- 顶部导航 -->
    <view class="page-header">
      <view class="header-content">
        <view>
          <text class="header-title">考证信息</text>
          <text class="header-desc">最新考试资讯，不错过报名时间</text>
        </view>
      </view>
    </view>
    
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar" @click="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索证书名称、主办方</text>
      </view>
      
      <!-- 分类筛选 -->
      <scroll-view class="category-scroll" scroll-x>
        <view class="category-list">
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === '' }"
            @click="selectCategory('')"
          >
            全部
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'language' }"
            @click="selectCategory('language')"
          >
            语言类
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'computer' }"
            @click="selectCategory('computer')"
          >
            计算机类
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'finance' }"
            @click="selectCategory('finance')"
          >
            财会类
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'law' }"
            @click="selectCategory('law')"
          >
            法律类
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'other' }"
            @click="selectCategory('other')"
          >
            其他
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 状态筛选 -->
    <view class="status-section">
      <scroll-view class="status-scroll" scroll-x>
        <view class="status-list">
          <view 
            class="status-item" 
            :class="{ 'status-active': activeStatus === '' }"
            @click="selectStatus('')"
          >
            全部状态
          </view>
          <view 
            class="status-item" 
            :class="{ 'status-active': activeStatus === 'upcoming' }"
            @click="selectStatus('upcoming')"
          >
            即将开始
          </view>
          <view 
            class="status-item" 
            :class="{ 'status-active': activeStatus === 'ongoing' }"
            @click="selectStatus('ongoing')"
          >
            报名中
          </view>
          <view 
            class="status-item" 
            :class="{ 'status-active': activeStatus === 'ended' }"
            @click="selectStatus('ended')"
          >
            已结束
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 考证列表 -->
    <scroll-view 
      class="cert-list" 
      scroll-y 
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载中 -->
      <view class="loading-tip" v-if="loading && certifications.length === 0">
        <text>加载中...</text>
      </view>
      
      <!-- 空状态 -->
      <view class="empty-state" v-if="!loading && certifications.length === 0">
        <text class="empty-icon">🏆</text>
        <text class="empty-text">暂无考证信息</text>
        <text class="empty-tip">下拉刷新试试</text>
      </view>
      
      <!-- 考证卡片列表 -->
      <view class="cert-cards" v-else>
        <view 
          class="cert-card" 
          v-for="cert in certifications" 
          :key="cert.id"
          @click="goToCertDetail(cert.id)"
        >
          <!-- 状态标签 -->
          <view class="cert-status-badge" :class="getStatusClass(cert.status)">
            <text class="status-text">{{ getStatusText(cert.status) }}</text>
          </view>
          
          <view class="cert-content">
            <view class="cert-info-main">
              <text class="cert-name">{{ cert.name }}</text>
              <text class="cert-category" v-if="cert.category">
                {{ getCategoryName(cert.category) }}
              </text>
            </view>
            
            <view class="cert-details">
              <view class="detail-item" v-if="cert.organizer">
                <text class="detail-icon">🏢</text>
                <text class="detail-text">{{ cert.organizer }}</text>
              </view>
              
              <view class="detail-row">
                <view class="detail-item" v-if="cert.registration_start">
                  <text class="detail-icon">📅</text>
                  <text class="detail-text">
                    报名: {{ formatDate(cert.registration_start) }}
                    <text v-if="cert.registration_end"> ~ {{ formatDate(cert.registration_end) }}</text>
                  </text>
                </view>
              </view>
              
              <view class="detail-row">
                <view class="detail-item" v-if="cert.exam_date">
                  <text class="detail-icon">📝</text>
                  <text class="detail-text">考试: {{ formatDate(cert.exam_date) }}</text>
                </view>
                
                <view class="detail-item" v-if="cert.fee !== null && cert.fee !== undefined">
                  <text class="detail-icon">💰</text>
                  <text class="detail-text">费用: ¥{{ cert.fee }}</text>
                </view>
              </view>
            </view>
            
            <view class="cert-actions" v-if="cert.requirements || cert.registration_url">
              <view class="action-left">
                <text class="req-text" v-if="cert.requirements" :numberOfLines="1">
                  💡 要求: {{ cert.requirements }}
                </text>
              </view>
              <view class="action-right" v-if="cert.registration_url">
                <view class="register-btn" @click.stop="openRegistration(cert.registration_url)">
                  <text class="register-text">立即报名</text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore">
        <text>加载更多...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && certifications.length > 0">
        <text>没有更多了</text>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 120rpx;"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { trainingApi } from '@/api/training'

const certifications = ref([])
const loading = ref(false)
const isRefreshing = ref(false)
const activeCategory = ref('')
const activeStatus = ref('')
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)

// 分类名称映射
const categoryNames = {
  language: '语言类',
  computer: '计算机类',
  finance: '财会类',
  law: '法律类',
  other: '其他'
}

// 状态样式映射
const statusClasses = {
  upcoming: 'status-upcoming',
  ongoing: 'status-ongoing',
  ended: 'status-ended'
}

// 状态文字映射
const statusTexts = {
  upcoming: '即将开始',
  ongoing: '报名中',
  ended: '已结束'
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryNames[category] || category
}

// 获取状态样式类
const getStatusClass = (status) => {
  return statusClasses[status] || 'status-upcoming'
}

// 获取状态文字
const getStatusText = (status) => {
  return statusTexts[status] || '即将开始'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${date.getFullYear()}-${month}-${day}`
}

// 选择分类
const selectCategory = (category) => {
  activeCategory.value = category
  page.value = 1
  hasMore.value = true
  certifications.value = []
  fetchCertifications()
}

// 选择状态
const selectStatus = (status) => {
  activeStatus.value = status
  page.value = 1
  hasMore.value = true
  certifications.value = []
  fetchCertifications()
}

// 获取考证列表
const fetchCertifications = async () => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    const params = {
      page: page.value,
      per_page: perPage.value
    }
    
    if (activeCategory.value) {
      params.category = activeCategory.value
    }
    
    if (activeStatus.value) {
      params.status = activeStatus.value
    }
    
    const res = await trainingApi.getCertifications(params)
    const data = res.data || res
    const newCerts = data.items || data || []
    
    if (page.value === 1) {
      certifications.value = newCerts
    } else {
      certifications.value = [...certifications.value, ...newCerts]
    }
    
    hasMore.value = newCerts.length >= perPage.value
  } catch (error) {
    console.error('获取考证信息列表失败:', error)
    uni.showToast({ title: '获取数据失败', icon: 'none' })
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
  fetchCertifications()
}

// 加载更多
const onLoadMore = () => {
  if (!hasMore.value || loading.value) return
  page.value++
  fetchCertifications()
}

// 页面跳转
const goToSearch = () => {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

const goToCertDetail = (certId) => {
  uni.showToast({ title: '考证详情功能开发中', icon: 'none' })
}

const openRegistration = (url) => {
  if (!url) return
  uni.showToast({ title: '即将跳转到报名页面', icon: 'none' })
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.navigateTo({
    url: `/pages/webview/index?url=${encodeURIComponent(url)}`
  })
  // #endif
}

onMounted(() => {
  fetchCertifications()
})
</script>

<style lang="scss" scoped>
.certifications-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 顶部导航
.page-header {
  background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%);
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

// 搜索栏
.search-section {
  background-color: #fff;
  padding: 24rpx 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 50rpx;
  padding: 16rpx 30rpx;
  margin-bottom: 24rpx;
}

.search-icon {
  font-size: 28rpx;
  margin-right: 16rpx;
}

.search-placeholder {
  font-size: 28rpx;
  color: #909399;
}

// 分类筛选
.category-scroll {
  white-space: nowrap;
}

.category-list {
  display: inline-flex;
  gap: 16rpx;
}

.category-item {
  padding: 12rpx 24rpx;
  background-color: #f5f7fa;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #606266;
  
  &.category-active {
    background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%);
    color: #fff;
  }
}

// 状态筛选
.status-section {
  background-color: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.status-scroll {
  white-space: nowrap;
}

.status-list {
  display: inline-flex;
  padding: 0 20rpx;
  gap: 16rpx;
}

.status-item {
  padding: 10rpx 24rpx;
  background-color: #f5f7fa;
  border-radius: 24rpx;
  font-size: 24rpx;
  color: #909399;
  
  &.status-active {
    background-color: #fef0f0;
    color: #f56c6c;
  }
}

// 考证列表
.cert-list {
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
}

// 考证卡片列表
.cert-cards {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.cert-card {
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  position: relative;
}

// 状态标签
.cert-status-badge {
  position: absolute;
  top: 0;
  right: 0;
  padding: 8rpx 24rpx;
  border-bottom-left-radius: 12rpx;
  
  &.status-upcoming {
    background-color: #409eff;
  }
  
  &.status-ongoing {
    background-color: #67c23a;
  }
  
  &.status-ended {
    background-color: #909399;
  }
}

.status-text {
  font-size: 22rpx;
  color: #fff;
}

.cert-content {
  padding: 24rpx;
}

.cert-info-main {
  margin-bottom: 16rpx;
}

.cert-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 8rpx;
}

.cert-category {
  font-size: 24rpx;
  color: #f56c6c;
  background-color: #fef0f0;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
}

.cert-details {
  margin-bottom: 16rpx;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  gap: 20rpx;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
  margin-bottom: 8rpx;
}

.detail-icon {
  font-size: 22rpx;
}

.detail-text {
  font-size: 24rpx;
  color: #909399;
}

// 操作区域
.cert-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1rpx solid #f5f5f5;
}

.action-left {
  flex: 1;
  min-width: 0;
}

.req-text {
  font-size: 24rpx;
  color: #909399;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.action-right {
  margin-left: 20rpx;
}

.register-btn {
  background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%);
  padding: 12rpx 28rpx;
  border-radius: 30rpx;
}

.register-text {
  font-size: 24rpx;
  color: #fff;
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
