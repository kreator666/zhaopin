<template>
  <view class="courses-page">
    <!-- 顶部导航 -->
    <view class="page-header">
      <view class="header-content">
        <view>
          <text class="header-title">精品课程</text>
          <text class="header-desc">海量优质课程，助力职业成长</text>
        </view>
        <view class="header-actions" v-if="userStore.isLoggedIn">
          <view class="action-btn" @click="goToMyCourses">
            <text class="action-icon">📚</text>
            <text class="action-text">我的课程</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar" @click="goToSearch">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索课程名称、讲师、描述</text>
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
            :class="{ 'category-active': activeCategory === 'exam_prep' }"
            @click="selectCategory('exam_prep')"
          >
            考试考证
          </view>
          <view 
            class="category-item" 
            :class="{ 'category-active': activeCategory === 'career' }"
            @click="selectCategory('career')"
          >
            职业技能
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
            :class="{ 'category-active': activeCategory === 'data' }"
            @click="selectCategory('data')"
          >
            数据科学
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 其他筛选 -->
    <view class="filter-section">
      <scroll-view class="filter-scroll" scroll-x>
        <view class="filter-list">
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeLevel === '' }"
            @click="selectLevel('')"
          >
            全部难度
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeLevel === 'beginner' }"
            @click="selectLevel('beginner')"
          >
            入门
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeLevel === 'intermediate' }"
            @click="selectLevel('intermediate')"
          >
            进阶
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeLevel === 'advanced' }"
            @click="selectLevel('advanced')"
          >
            高级
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 课程列表 -->
    <scroll-view 
      class="course-list" 
      scroll-y 
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载中 -->
      <view class="loading-tip" v-if="loading && courses.length === 0">
        <text>加载中...</text>
      </view>
      
      <!-- 空状态 -->
      <view class="empty-state" v-if="!loading && courses.length === 0">
        <text class="empty-icon">📚</text>
        <text class="empty-text">暂无课程</text>
        <text class="empty-tip">下拉刷新试试</text>
      </view>
      
      <!-- 课程卡片网格 -->
      <view class="course-grid" v-else>
        <view 
          class="course-card" 
          v-for="course in courses" 
          :key="course.id"
          @click="goToCourseDetail(course.id)"
        >
          <view class="course-cover">
            <image 
              :src="getCoverImage(course.cover_image)" 
              mode="aspectFill" 
              class="cover-img"
            />
            <view class="course-tags">
              <view class="tag-item online" v-if="course.is_online">
                线上
              </view>
              <view class="tag-item offline" v-else>
                线下
              </view>
              <view class="tag-item free" v-if="course.price === 0">
                免费
              </view>
            </view>
          </view>
          
          <view class="course-info">
            <text class="course-title">{{ course.title }}</text>
            <view class="course-meta" v-if="course.instructor || course.provider">
              <text class="course-instructor">{{ course.instructor || course.provider }}</text>
            </view>
            <view class="course-footer">
              <view class="course-price" v-if="course.price > 0">
                <text class="price-current">¥{{ course.price }}</text>
                <text class="price-original" v-if="course.original_price && course.original_price > course.price">
                  ¥{{ course.original_price }}
                </text>
              </view>
              <view class="course-price free" v-else>
                <text class="price-free">免费</text>
              </view>
              <view class="course-stats">
                <text class="stat-text">{{ course.enrolled_count || 0 }}人学习</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore">
        <text>加载更多...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && courses.length > 0">
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

const courses = ref([])
const loading = ref(false)
const isRefreshing = ref(false)
const activeCategory = ref('')
const activeLevel = ref('')
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)

// 分类名称映射
const categoryMap = {
  programming: '编程开发',
  language: '语言学习',
  exam_prep: '考试考证',
  career: '职业技能',
  design: '设计创意',
  data: '数据科学'
}

// 检测当前运行环境
const isH5 = typeof window !== 'undefined' && typeof window.document !== 'undefined'

// 获取封面图片
const getCoverImage = (image) => {
  if (!image) return ''
  if (image.startsWith('http')) return image
  // H5 模式使用相对路径，依赖 Vite 代理
  if (isH5) {
    return image
  }
  // 小程序模式使用完整 URL
  return 'http://localhost:5000' + image
}

// 选择分类
const selectCategory = (category) => {
  activeCategory.value = category
  page.value = 1
  hasMore.value = true
  courses.value = []
  fetchCourses()
}

// 选择难度
const selectLevel = (level) => {
  activeLevel.value = level
  page.value = 1
  hasMore.value = true
  courses.value = []
  fetchCourses()
}

// 获取课程列表
const fetchCourses = async () => {
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
    
    if (activeLevel.value) {
      params.level = activeLevel.value
    }
    
    const res = await trainingApi.getCourses(params)
    const data = res.data || res
    const newCourses = data.items || data || []
    
    if (page.value === 1) {
      courses.value = newCourses
    } else {
      courses.value = [...courses.value, ...newCourses]
    }
    
    hasMore.value = newCourses.length >= perPage.value
  } catch (error) {
    console.error('获取课程列表失败:', error)
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
  fetchCourses()
}

// 加载更多
const onLoadMore = () => {
  if (!hasMore.value || loading.value) return
  page.value++
  fetchCourses()
}

// 页面跳转
const goToSearch = () => {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

const goToMyCourses = () => {
  uni.showToast({ title: '我的课程功能开发中', icon: 'none' })
}

const goToCourseDetail = (courseId) => {
  uni.showToast({ title: '课程详情功能开发中', icon: 'none' })
}

onMounted(() => {
  fetchCourses()
})
</script>

<style lang="scss" scoped>
.courses-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 顶部导航
.page-header {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
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
    background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
    color: #fff;
  }
}

// 其他筛选
.filter-section {
  background-color: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.filter-scroll {
  white-space: nowrap;
}

.filter-list {
  display: inline-flex;
  padding: 0 20rpx;
  gap: 16rpx;
}

.filter-item {
  padding: 10rpx 24rpx;
  background-color: #f5f7fa;
  border-radius: 24rpx;
  font-size: 24rpx;
  color: #909399;
  
  &.filter-active {
    background-color: #ecf5ff;
    color: #409eff;
  }
}

// 课程列表
.course-list {
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

// 课程网格
.course-grid {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.course-card {
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.course-cover {
  position: relative;
  width: 100%;
  height: 320rpx;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.course-tags {
  position: absolute;
  top: 16rpx;
  left: 16rpx;
  display: flex;
  gap: 8rpx;
}

.tag-item {
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  color: #fff;
  
  &.online {
    background-color: rgba(64, 158, 255, 0.9);
  }
  
  &.offline {
    background-color: rgba(230, 162, 60, 0.9);
  }
  
  &.free {
    background-color: rgba(103, 194, 58, 0.9);
  }
}

.course-info {
  padding: 20rpx;
}

.course-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.course-meta {
  margin-bottom: 16rpx;
}

.course-instructor {
  font-size: 24rpx;
  color: #909399;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-price {
  display: flex;
  align-items: baseline;
  
  &.free {
    .price-free {
      font-size: 28rpx;
      font-weight: bold;
      color: #67c23a;
    }
  }
}

.price-current {
  font-size: 32rpx;
  font-weight: bold;
  color: #f56c6c;
}

.price-original {
  font-size: 22rpx;
  color: #c0c4cc;
  text-decoration: line-through;
  margin-left: 8rpx;
}

.course-stats {
  .stat-text {
    font-size: 22rpx;
    color: #c0c4cc;
  }
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
