<template>
  <view class="jobs-page">
    <!-- 搜索栏 -->
    <view class="search-bar" @click="goToSearch">
      <view class="search-input">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索职位、公司名称...</text>
      </view>
    </view>
    
    <!-- 筛选栏 -->
    <view class="filter-bar">
      <scroll-view class="filter-scroll" scroll-x>
        <view class="filter-list">
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeFilter === 'all' }"
            @click="selectFilter('all')"
          >
            全部
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeFilter === 'new' }"
            @click="selectFilter('new')"
          >
            最新
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeFilter === 'hot' }"
            @click="selectFilter('hot')"
          >
            热门
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeFilter === 'intern' }"
            @click="selectFilter('intern')"
          >
            实习
          </view>
          <view 
            class="filter-item" 
            :class="{ 'filter-active': activeFilter === 'remote' }"
            @click="selectFilter('remote')"
          >
            远程
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 职位列表 -->
    <scroll-view 
      class="job-list" 
      scroll-y 
      :refresher-enabled="true"
      :refresher-triggered="isRefreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <!-- 加载中 -->
      <view class="loading-tip" v-if="loading && jobs.length === 0">
        <text>加载中...</text>
      </view>
      
      <!-- 空状态 -->
      <view class="empty-state" v-if="!loading && jobs.length === 0">
        <text class="empty-icon">📭</text>
        <text class="empty-text">暂无职位</text>
        <text class="empty-tip">下拉刷新试试</text>
      </view>
      
      <!-- 职位卡片列表 -->
      <view class="job-cards">
        <view 
          class="job-card" 
          v-for="job in jobs" 
          :key="job.id"
          @click="goToJobDetail(job.id)"
        >
          <view class="job-header">
            <text class="job-title">{{ job.title }}</text>
            <view class="job-salary" v-if="job.salary_min && job.salary_max">
              <text class="salary-text">{{ job.salary_min }}-{{ job.salary_max }}</text>
              <text class="salary-unit">K/月</text>
            </view>
            <text class="job-salary negotiate" v-else>薪资面议</text>
          </view>
          
          <view class="job-info">
            <text class="job-company">{{ job.company_name || '企业' }}</text>
            <text class="job-location">{{ job.location || '地点待定' }}</text>
          </view>
          
          <view class="job-tags" v-if="job.tags && job.tags.length > 0">
            <text class="job-tag" v-for="(tag, idx) in job.tags.slice(0, 4)" :key="idx">{{ tag }}</text>
          </view>
          
          <view class="job-footer">
            <text class="job-time">{{ formatTime(job.created_at) }}</text>
            <view class="job-actions">
              <view class="action-btn favorite" @click.stop="toggleFavorite(job)">
                <text class="action-icon">{{ job.is_favorite ? '❤️' : '🤍' }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore">
        <text>加载更多...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && jobs.length > 0">
        <text>没有更多了</text>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 120rpx;"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi } from '@/api/jobs'

const jobs = ref([])
const loading = ref(false)
const isRefreshing = ref(false)
const activeFilter = ref('all')
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  // 一天内
  if (diff < 24 * 60 * 60 * 1000) {
    const hours = Math.floor(diff / (60 * 60 * 1000))
    if (hours < 1) return '刚刚'
    return `${hours}小时前`
  }
  
  // 一周内
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days}天前`
  }
  
  // 格式化日期
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}月${day}日`
}

// 选择筛选
const selectFilter = (filter) => {
  activeFilter.value = filter
  page.value = 1
  hasMore.value = true
  jobs.value = []
  fetchJobs()
}

// 获取职位列表
const fetchJobs = async () => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    const params = {
      page: page.value,
      per_page: perPage.value
    }
    
    // 根据筛选条件添加参数
    if (activeFilter.value === 'new') {
      params.sort = 'new'
    } else if (activeFilter.value === 'hot') {
      params.sort = 'hot'
    }
    
    const res = await jobsApi.getJobs(params)
    const data = res.data || res
    const newJobs = data.items || data || []
    
    if (page.value === 1) {
      jobs.value = newJobs
    } else {
      jobs.value = [...jobs.value, ...newJobs]
    }
    
    hasMore.value = newJobs.length >= perPage.value
  } catch (error) {
    console.error('获取职位列表失败:', error)
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
  fetchJobs()
}

// 加载更多
const onLoadMore = () => {
  if (!hasMore.value || loading.value) return
  page.value++
  fetchJobs()
}

// 页面跳转
const goToSearch = () => {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

const goToJobDetail = (jobId) => {
  uni.showToast({ title: '职位详情功能开发中', icon: 'none' })
}

// 收藏/取消收藏
const toggleFavorite = async (job) => {
  try {
    await jobsApi.toggleFavorite(job.id)
    job.is_favorite = !job.is_favorite
    uni.showToast({
      title: job.is_favorite ? '已收藏' : '已取消收藏',
      icon: 'success'
    })
  } catch (error) {
    console.error('收藏失败:', error)
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style lang="scss" scoped>
.jobs-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

// 搜索栏
.search-bar {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 20rpx 30rpx;
  padding-top: 40rpx;
}

.search-input {
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 50rpx;
  padding: 16rpx 30rpx;
}

.search-icon {
  font-size: 28rpx;
  margin-right: 16rpx;
}

.search-placeholder {
  font-size: 28rpx;
  color: #909399;
}

// 筛选栏
.filter-bar {
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
  padding: 12rpx 28rpx;
  background-color: #f5f7fa;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #606266;
  
  &.filter-active {
    background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
    color: #fff;
  }
}

// 职位列表
.job-list {
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

// 职位卡片
.job-cards {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.job-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 28rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.job-title {
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
  margin-right: 20rpx;
}

.job-salary {
  display: flex;
  align-items: baseline;
  
  &.negotiate {
    font-size: 26rpx;
    color: #909399;
  }
}

.salary-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #f56c6c;
}

.salary-unit {
  font-size: 22rpx;
  color: #f56c6c;
  margin-left: 4rpx;
}

.job-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.job-company {
  font-size: 28rpx;
  color: #606266;
}

.job-location {
  font-size: 26rpx;
  color: #909399;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.job-tag {
  font-size: 22rpx;
  color: #909399;
  background-color: #f5f7fa;
  padding: 6rpx 16rpx;
  border-radius: 4rpx;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1rpx solid #f0f0f0;
}

.job-time {
  font-size: 24rpx;
  color: #c0c4cc;
}

.job-actions {
  display: flex;
  gap: 20rpx;
}

.action-btn {
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
}

.action-icon {
  font-size: 32rpx;
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
