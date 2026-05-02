<template>
  <view class="cert-detail-page">
    <!-- 加载中 -->
    <view class="loading-container" v-if="loading">
      <text class="loading-text">加载中...</text>
    </view>
    
    <!-- 内容区域 -->
    <view class="content-container" v-else>
      <!-- 头部信息 -->
      <view class="header-section">
        <view class="status-badge" :class="getStatusClass(cert.status)">
          <text class="status-text">{{ getStatusText(cert.status) }}</text>
        </view>
        
        <text class="cert-name">{{ cert.name }}</text>
        
        <view class="meta-row" v-if="cert.organizer">
          <text class="meta-icon">🏢</text>
          <text class="meta-text">{{ cert.organizer }}</text>
        </view>
        
        <view class="meta-row" v-if="cert.category">
          <text class="meta-icon">📋</text>
          <text class="meta-text">{{ getCategoryName(cert.category) }}</text>
        </view>
      </view>
      
      <!-- 关键时间轴 -->
      <view class="timeline-section" v-if="cert.registration_start || cert.exam_date">
        <view class="section-title">重要时间</view>
        
        <view class="timeline-list">
          <view class="timeline-item" v-if="cert.registration_start">
            <view class="timeline-dot registration"></view>
            <view class="timeline-content">
              <text class="timeline-title">报名时间</text>
              <text class="timeline-date">
                {{ formatDate(cert.registration_start) }}
                <text v-if="cert.registration_end"> ~ {{ formatDate(cert.registration_end) }}</text>
              </text>
            </view>
          </view>
          
          <view class="timeline-divider" v-if="cert.registration_start && cert.exam_date"></view>
          
          <view class="timeline-item" v-if="cert.exam_date">
            <view class="timeline-dot exam"></view>
            <view class="timeline-content">
              <text class="timeline-title">考试日期</text>
              <text class="timeline-date">{{ formatDate(cert.exam_date) }}</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 费用信息 -->
      <view class="fee-section" v-if="cert.fee !== null && cert.fee !== undefined">
        <view class="section-title">报名费用</view>
        <view class="fee-content">
          <text class="fee-currency">¥</text>
          <text class="fee-value">{{ cert.fee }}</text>
        </view>
      </view>
      
      <!-- 证书介绍 -->
      <view class="detail-section" v-if="cert.description">
        <view class="section-title">证书介绍</view>
        <text class="detail-content">{{ cert.description }}</text>
      </view>
      
      <!-- 报名要求 -->
      <view class="detail-section" v-if="cert.requirements">
        <view class="section-title">报名要求</view>
        <text class="detail-content">{{ cert.requirements }}</text>
      </view>
      
      <!-- 其他信息 -->
      <view class="info-section" v-if="cert.registration_url || cert.created_at">
        <view class="section-title">其他信息</view>
        <view class="info-list">
          <view class="info-item" v-if="cert.created_at">
            <text class="info-label">发布时间</text>
            <text class="info-value">{{ formatDate(cert.created_at) }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 底部操作栏 -->
    <view class="action-bar" v-if="cert.registration_url">
      <view 
        class="action-btn primary" 
        :class="{ disabled: cert.status === 'ended' }"
        @click="openRegistration"
      >
        <text class="action-icon">📝</text>
        <text class="action-text">{{ cert.status === 'ended' ? '报名已结束' : '立即报名' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { trainingApi } from '@/api/training'

const cert = ref({})
const loading = ref(true)

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
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取考证详情
const fetchCertDetail = async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const certId = currentPage.options.id
  
  if (!certId) {
    uni.showToast({ title: '参数错误', icon: 'none' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
    return
  }
  
  loading.value = true
  
  try {
    const res = await trainingApi.getCertificationDetail(certId)
    const data = res.data || res
    cert.value = data
  } catch (error) {
    console.error('获取考证信息详情失败:', error)
    uni.showToast({ title: '获取详情失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// 打开报名链接
const openRegistration = () => {
  if (!cert.value.registration_url) {
    uni.showToast({ title: '暂无报名链接', icon: 'none' })
    return
  }
  
  if (cert.value.status === 'ended') {
    uni.showToast({ title: '报名已结束', icon: 'none' })
    return
  }
  
  const url = cert.value.registration_url
  uni.showToast({ title: '正在打开报名页面...', icon: 'none' })
  
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  
  // #ifndef H5
  // 小程序模式：跳转到 webview 页面
  uni.navigateTo({
    url: `/pages/webview/index?url=${encodeURIComponent(url)}`
  })
  // #endif
}

onMounted(() => {
  fetchCertDetail()
})
</script>

<style lang="scss" scoped>
.cert-detail-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 140rpx;
}

// 加载中
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.loading-text {
  font-size: 28rpx;
  color: #909399;
}

// 内容容器
.content-container {
  padding: 20rpx;
}

// 头部区域
.header-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  position: relative;
}

.status-badge {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  
  &.status-upcoming {
    background-color: #ecf5ff;
  }
  
  &.status-ongoing {
    background-color: #f0f9eb;
  }
  
  &.status-ended {
    background-color: #f4f4f5;
  }
}

.status-text {
  font-size: 24rpx;
  
  .status-upcoming & {
    color: #409eff;
  }
  
  .status-ongoing & {
    color: #67c23a;
  }
  
  .status-ended & {
    color: #909399;
  }
}

.cert-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
  padding-right: 160rpx;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 12rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.meta-icon {
  font-size: 24rpx;
}

.meta-text {
  font-size: 26rpx;
  color: #909399;
}

// 时间轴区域
.timeline-section,
.fee-section,
.detail-section,
.info-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.timeline-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.timeline-item {
  display: flex;
  gap: 20rpx;
  padding: 16rpx 0;
}

.timeline-dot {
  width: 24rpx;
  height: 24rpx;
  border-radius: 50%;
  margin-top: 8rpx;
  flex-shrink: 0;
  
  &.registration {
    background-color: #409eff;
    box-shadow: 0 0 0 6rpx rgba(64, 158, 255, 0.2);
  }
  
  &.exam {
    background-color: #f56c6c;
    box-shadow: 0 0 0 6rpx rgba(245, 108, 108, 0.2);
  }
}

.timeline-divider {
  width: 2rpx;
  height: 40rpx;
  background-color: #e4e7ed;
  margin-left: 11rpx;
}

.timeline-content {
  flex: 1;
}

.timeline-title {
  font-size: 28rpx;
  color: #606266;
  display: block;
  margin-bottom: 8rpx;
}

.timeline-date {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
}

// 费用区域
.fee-content {
  display: flex;
  align-items: baseline;
  justify-content: center;
  padding: 20rpx 0;
}

.fee-currency {
  font-size: 32rpx;
  color: #f56c6c;
  font-weight: bold;
}

.fee-value {
  font-size: 56rpx;
  color: #f56c6c;
  font-weight: bold;
}

// 详情内容
.detail-content {
  font-size: 28rpx;
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
}

// 信息列表
.info-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 28rpx;
  color: #909399;
}

.info-value {
  font-size: 28rpx;
  color: #333;
}

// 底部操作栏
.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 20rpx 30rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  display: flex;
  justify-content: center;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 24rpx 80rpx;
  border-radius: 50rpx;
  
  &.primary {
    background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%);
    
    &.disabled {
      background-color: #c0c4cc;
      background: none;
    }
  }
}

.action-icon {
  font-size: 36rpx;
}

.action-text {
  font-size: 30rpx;
  color: #fff;
  font-weight: 500;
}
</style>
