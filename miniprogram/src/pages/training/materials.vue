<template>
  <view class="materials-page">
    <!-- 顶部导航 -->
    <view class="page-header">
      <view class="header-content">
        <view>
          <text class="header-title">学习资料</text>
          <text class="header-desc">海量学习资料，助力学习成长</text>
        </view>
        <view class="header-actions" v-if="userStore.isLoggedIn">
          <view class="action-btn" @click="goToMyMaterials">
            <text class="action-icon">📤</text>
            <text class="action-text">我的资料</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar" @click="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索资料名称、描述</text>
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
            :class="{ 'category-active': activeCategory === 'programming' }"
            @click="selectCategory('programming')"
          >
            编程开发
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'language' }"
            @click="selectCategory('language')"
          >
            语言学习
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'exam' }"
            @click="selectCategory('exam')"
          >
            考试资料
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'design' }"
            @click="selectCategory('design')"
          >
            设计创意
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'other' }"
            @click="selectCategory('other')"
          >
            其他资料
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 资料列表 -->
    <scroll-view 
      class="material-list" 
      scroll-y 
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载中 -->
      <view class="loading-tip" v-if="loading && materials.length === 0">
        <text>加载中...</text>
      </view>
      
      <!-- 空状态 -->
      <view class="empty-state" v-if="!loading && materials.length === 0">
        <text class="empty-icon">📄</text>
        <text class="empty-text">暂无学习资料</text>
        <text class="empty-tip">下拉刷新试试</text>
      </view>
      
      <!-- 资料卡片列表 -->
      <view class="material-cards" v-else>
        <view 
          class="material-card" 
          v-for="material in materials" 
          :key="material.id"
          @click="goToMaterialDetail(material.id)"
        >
          <view class="material-icon-wrapper">
            <text class="material-icon">{{ getFileIcon(material.file_type) }}</text>
            <text class="material-type">{{ getFileTypeName(material.file_type) }}</text>
          </view>
          
          <view class="material-info">
            <text class="material-title">{{ material.title }}</text>
            <text class="material-desc" v-if="material.description">
              {{ material.description }}
            </text>
            
            <view class="material-meta">
              <view class="meta-left">
                <view class="meta-item" v-if="material.user">
                  <text class="meta-icon">👤</text>
                  <text class="meta-text">{{ material.user.username }}</text>
                </view>
                <view class="meta-item" v-if="material.file_size">
                  <text class="meta-icon">📦</text>
                  <text class="meta-text">{{ material.file_size }}</text>
                </view>
              </view>
              <view class="meta-right">
                <view class="meta-stat">
                  <text class="stat-icon">⬇️</text>
                  <text class="stat-text">{{ material.download_count || 0 }}</text>
                </view>
                <view class="meta-stat">
                  <text class="stat-icon">❤️</text>
                  <text class="stat-text">{{ material.like_count || 0 }}</text>
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
      
      <view class="no-more" v-if="!hasMore && materials.length > 0">
        <text>没有更多了</text>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 120rpx;"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { trainingApi } from '@/api/training'

const userStore = useUserStore()

const materials = ref([])
const loading = ref(false)
const isRefreshing = ref(false)
const activeCategory = ref('')
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)

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
  pdf: 'PDF',
  doc: 'Word',
  docx: 'Word',
  xls: 'Excel',
  xlsx: 'Excel',
  ppt: 'PPT',
  pptx: 'PPT',
  video: '视频',
  mp4: '视频',
  image: '图片',
  jpg: '图片',
  png: '图片',
  zip: '压缩包',
  rar: '压缩包',
  other: '文件'
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

// 选择分类
const selectCategory = (category) => {
  activeCategory.value = category
  page.value = 1
  hasMore.value = true
  materials.value = []
  fetchMaterials()
}

// 获取资料列表
const fetchMaterials = async () => {
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
    
    const res = await trainingApi.getMaterials(params)
    const data = res.data || res
    const newMaterials = data.items || data || []
    
    if (page.value === 1) {
      materials.value = newMaterials
    } else {
      materials.value = [...materials.value, ...newMaterials]
    }
    
    hasMore.value = newMaterials.length >= perPage.value
  } catch (error) {
    console.error('获取学习资料列表失败:', error)
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
  fetchMaterials()
}

// 加载更多
const onLoadMore = () => {
  if (!hasMore.value || loading.value) return
  page.value++
  fetchMaterials()
}

// 页面跳转
const goToSearch = () => {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

const goToMyMaterials = () => {
  uni.showToast({ title: '我的资料功能开发中', icon: 'none' })
}

const goToMaterialDetail = (materialId) => {
  uni.showToast({ title: '资料详情功能开发中', icon: 'none' })
}

onMounted(() => {
  fetchMaterials()
})
</script>

<style lang="scss" scoped>
.materials-page {
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12rpx 20rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12rpx;
}

.action-icon {
  font-size: 32rpx;
  margin-bottom: 4rpx;
}

.action-text {
  font-size: 22rpx;
  color: #fff;
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
    background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
    color: #fff;
  }
}

// 资料列表
.material-list {
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

// 资料卡片列表
.material-cards {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.material-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  display: flex;
  gap: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.material-icon-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100rpx;
  height: 100rpx;
  background-color: #f0f9eb;
  border-radius: 12rpx;
  flex-shrink: 0;
}

.material-icon {
  font-size: 44rpx;
  margin-bottom: 4rpx;
}

.material-type {
  font-size: 20rpx;
  color: #67c23a;
}

.material-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.material-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 8rpx;
}

.material-desc {
  font-size: 24rpx;
  color: #909399;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.material-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-left {
  display: flex;
  gap: 20rpx;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
}

.meta-icon {
  font-size: 22rpx;
}

.meta-text {
  font-size: 22rpx;
  color: #909399;
}

.meta-right {
  display: flex;
  gap: 20rpx;
}

.meta-stat {
  display: flex;
  align-items: center;
  gap: 4rpx;
}

.stat-icon {
  font-size: 20rpx;
}

.stat-text {
  font-size: 22rpx;
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
