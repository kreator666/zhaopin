<template>
  <view class="material-detail-page">
    <!-- 加载中 -->
    <view class="loading-container" v-if="loading">
      <text class="loading-text">加载中...</text>
    </view>
    
    <!-- 内容区域 -->
    <view class="content-container" v-else>
      <!-- 头部信息 -->
      <view class="header-section">
        <view class="icon-wrapper">
          <text class="material-icon">{{ getFileIcon(material.file_type) }}</text>
          <text class="material-type">{{ getFileTypeName(material.file_type) }}</text>
        </view>
        
        <view class="info-wrapper">
          <text class="material-title">{{ material.title }}</text>
          <view class="meta-row" v-if="material.user">
            <text class="meta-icon">👤</text>
            <text class="meta-text">{{ material.user.username }}</text>
          </view>
        </view>
      </view>
      
      <!-- 统计信息 -->
      <view class="stats-section">
        <view class="stat-item">
          <text class="stat-value">{{ material.download_count || 0 }}</text>
          <text class="stat-label">下载次数</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <text class="stat-value">{{ material.like_count || 0 }}</text>
          <text class="stat-label">点赞数</text>
        </view>
        <view class="stat-divider" v-if="material.file_size"></view>
        <view class="stat-item" v-if="material.file_size">
          <text class="stat-value">{{ material.file_size }}</text>
          <text class="stat-label">文件大小</text>
        </view>
      </view>
      
      <!-- 详细信息 -->
      <view class="detail-section">
        <view class="section-title">资料介绍</view>
        <text class="detail-content" v-if="material.description">{{ material.description }}</text>
        <text class="detail-empty" v-else>暂无介绍</text>
      </view>
      
      <!-- 其他信息 -->
      <view class="info-section" v-if="material.category || material.created_at">
        <view class="section-title">其他信息</view>
        <view class="info-list">
          <view class="info-item" v-if="material.category">
            <text class="info-label">资料分类</text>
            <text class="info-value">{{ getCategoryName(material.category) }}</text>
          </view>
          <view class="info-item" v-if="material.created_at">
            <text class="info-label">上传时间</text>
            <text class="info-value">{{ formatDate(material.created_at) }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 底部操作栏 -->
    <view class="action-bar">
      <view class="action-left">
        <view class="action-btn small" @click="handleLike">
          <text class="action-icon">{{ isLiked ? '❤️' : '🤍' }}</text>
          <text class="action-text">点赞</text>
        </view>
      </view>
      
      <view class="action-right">
        <view 
          class="action-btn primary" 
          :class="{ disabled: !material.file_url }"
          @click="handleDownload"
        >
          <text class="action-icon">⬇️</text>
          <text class="action-text">下载资料</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { trainingApi } from '@/api/training'

const userStore = useUserStore()

const material = ref({})
const loading = ref(true)
const isLiked = ref(false)

// 文件类型图标映射
const fileTypeIcons = {
  pdf: '📑',
  doc: '📝',
  docx: '📝',
  xls: '📊',
  xlsx: '📊',
  ppt: '📽️',
  pptx: '📽️',
  video: '🎬',
  mp4: '🎬',
  image: '🖼️',
  jpg: '🖼️',
  png: '🖼️',
  zip: '📦',
  rar: '📦',
  other: '📄'
}

// 文件类型名称映射
const fileTypeNames = {
  pdf: 'PDF文档',
  doc: 'Word文档',
  docx: 'Word文档',
  xls: 'Excel表格',
  xlsx: 'Excel表格',
  ppt: 'PPT演示',
  pptx: 'PPT演示',
  video: '视频文件',
  mp4: '视频文件',
  image: '图片文件',
  jpg: '图片文件',
  png: '图片文件',
  zip: '压缩包',
  rar: '压缩包',
  other: '其他文件'
}

// 分类名称映射
const categoryNames = {
  programming: '编程开发',
  language: '语言学习',
  exam: '考试资料',
  design: '设计创意',
  other: '其他资料'
}

// 获取文件图标
const getFileIcon = (fileType) => {
  if (!fileType) return '📄'
  const type = fileType.toLowerCase()
  return fileTypeIcons[type] || fileTypeIcons.other
}

// 获取文件类型名称
const getFileTypeName = (fileType) => {
  if (!fileType) return '文件'
  const type = fileType.toLowerCase()
  return fileTypeNames[type] || '文件'
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryNames[category] || category
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hour = date.getHours().toString().padStart(2, '0')
  const minute = date.getMinutes().toString().padStart(2, '0')
  return `${year}-${month}-${day} ${hour}:${minute}`
}

// 获取资料详情
const fetchMaterialDetail = async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const materialId = currentPage.options.id
  
  if (!materialId) {
    uni.showToast({ title: '参数错误', icon: 'none' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
    return
  }
  
  loading.value = true
  
  try {
    const res = await trainingApi.getMaterialDetail(materialId)
    const data = res.data || res
    material.value = data
  } catch (error) {
    console.error('获取学习资料详情失败:', error)
    uni.showToast({ title: '获取详情失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// 点赞
const handleLike = async () => {
  if (!userStore.isLoggedIn) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    setTimeout(() => {
      uni.navigateTo({ url: '/pages/login/index' })
    }, 1500)
    return
  }
  
  if (isLiked.value) {
    uni.showToast({ title: '已经点赞过了', icon: 'none' })
    return
  }
  
  try {
    const res = await trainingApi.likeMaterial(material.value.id)
    isLiked.value = true
    material.value.like_count = (material.value.like_count || 0) + 1
    uni.showToast({ title: '点赞成功', icon: 'success' })
  } catch (error) {
    console.error('点赞失败:', error)
    uni.showToast({ title: error?.error || '点赞失败', icon: 'none' })
  }
}

// 下载
const handleDownload = async () => {
  if (!material.value.file_url) {
    uni.showToast({ title: '暂无下载链接', icon: 'none' })
    return
  }
  
  try {
    // 调用下载计数 API
    await trainingApi.downloadMaterial(material.value.id)
    
    // 更新下载计数
    material.value.download_count = (material.value.download_count || 0) + 1
    
    // 处理下载链接
    const isH5 = typeof window !== 'undefined' && typeof window.document !== 'undefined'
    let downloadUrl = material.value.file_url
    
    // H5 模式下，如果是相对路径，不需要添加前缀（Vite 代理会处理）
    // 小程序模式下，如果是相对路径，需要添加完整 URL
    if (!isH5 && !downloadUrl.startsWith('http')) {
      downloadUrl = 'http://localhost:5000' + downloadUrl
    }
    
    uni.showToast({ title: '正在打开下载链接...', icon: 'none' })
    
    // #ifdef H5
    // H5 模式：直接在新窗口打开
    window.open(downloadUrl, '_blank')
    // #endif
    
    // #ifndef H5
    // 小程序模式：下载文件
    uni.downloadFile({
      url: downloadUrl,
      success: (res) => {
        if (res.statusCode === 200) {
          const filePath = res.tempFilePath
          uni.openDocument({
            filePath: filePath,
            showMenu: true,
            success: () => {
              console.log('打开文档成功')
            },
            fail: (err) => {
              console.error('打开文档失败:', err)
              uni.showToast({ title: '无法打开该文件类型', icon: 'none' })
            }
          })
        }
      },
      fail: (err) => {
        console.error('下载文件失败:', err)
        uni.showToast({ title: '下载失败', icon: 'none' })
      }
    })
    // #endif
    
  } catch (error) {
    console.error('下载失败:', error)
    uni.showToast({ title: '下载失败', icon: 'none' })
  }
}

onMounted(() => {
  fetchMaterialDetail()
})
</script>

<style lang="scss" scoped>
.material-detail-page {
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
  display: flex;
  gap: 24rpx;
  margin-bottom: 20rpx;
}

.icon-wrapper {
  width: 120rpx;
  height: 120rpx;
  background-color: #f0f9eb;
  border-radius: 16rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.material-icon {
  font-size: 52rpx;
  margin-bottom: 4rpx;
}

.material-type {
  font-size: 20rpx;
  color: #67c23a;
}

.info-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.material-title {
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.meta-icon {
  font-size: 24rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #909399;
}

// 统计区域
.stats-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 20rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 4rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #909399;
}

.stat-divider {
  width: 1rpx;
  height: 60rpx;
  background-color: #f0f0f0;
}

// 详细信息区域
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

.detail-content {
  font-size: 28rpx;
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
}

.detail-empty {
  font-size: 28rpx;
  color: #c0c4cc;
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
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.action-left,
.action-right {
  display: flex;
  gap: 16rpx;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 20rpx 40rpx;
  border-radius: 40rpx;
  background-color: #f5f7fa;
  
  &.small {
    padding: 16rpx 32rpx;
  }
  
  &.primary {
    background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
    
    &.disabled {
      background-color: #c0c4cc;
      background: none;
    }
  }
}

.action-icon {
  font-size: 32rpx;
}

.action-text {
  font-size: 28rpx;
  color: #606266;
  
  .primary & {
    color: #fff;
    
    .disabled & {
      color: #fff;
    }
  }
}
</style>
