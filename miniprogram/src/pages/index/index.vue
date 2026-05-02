<template>
  <view class="home-page">
    <!-- 顶部搜索栏 -->
    <view class="search-bar" @click="goToSearch">
      <view class="search-input">
        <text class="search-icon">🔍</text>
        <text class="search-placeholder">搜索职位、课程、资料...</text>
      </view>
    </view>
    
    <!-- 轮播图 -->
    <view class="banner-section">
      <swiper class="banner-swiper" indicator-dots autoplay circular>
        <swiper-item v-for="(item, index) in banners" :key="index">
          <view class="banner-item" :style="{ background: item.color }">
            <text class="banner-title">{{ item.title }}</text>
            <text class="banner-desc">{{ item.desc }}</text>
          </view>
        </swiper-item>
      </swiper>
    </view>
    
    <!-- 功能入口 -->
    <view class="entry-section">
      <view class="section-title">热门服务</view>
      <view class="entry-grid">
        <view class="entry-item" @click="goToJobs">
          <view class="entry-icon job-icon">
            <text class="icon-text">💼</text>
          </view>
          <text class="entry-text">找工作</text>
        </view>
        
        <view class="entry-item" @click="goToCourses">
          <view class="entry-icon course-icon">
            <text class="icon-text">📚</text>
          </view>
          <text class="entry-text">精品课程</text>
        </view>
        
        <view class="entry-item" @click="goToMaterials">
          <view class="entry-icon material-icon">
            <text class="icon-text">📄</text>
          </view>
          <text class="entry-text">学习资料</text>
        </view>
        
        <view class="entry-item" @click="goToCertifications">
          <view class="entry-icon cert-icon">
            <text class="icon-text">🏆</text>
          </view>
          <text class="entry-text">考证信息</text>
        </view>
        
        <view class="entry-item" @click="goToSocial">
          <view class="entry-icon social-icon">
            <text class="icon-text">💬</text>
          </view>
          <text class="entry-text">社交动态</text>
        </view>
        
        <view class="entry-item" @click="goToFlea">
          <view class="entry-icon flea-icon">
            <text class="icon-text">🏪</text>
          </view>
          <text class="entry-text">跳蚤市场</text>
        </view>
        
        <view class="entry-item" @click="goToCampusTalks">
          <view class="entry-icon talk-icon">
            <text class="icon-text">🏫</text>
          </view>
          <text class="entry-text">校园宣讲</text>
        </view>
        
        <view class="entry-item" @click="goToInterviews">
          <view class="entry-icon interview-icon">
            <text class="icon-text">🎯</text>
          </view>
          <text class="entry-text">面试经验</text>
        </view>
      </view>
    </view>
    
    <!-- 热门职位 -->
    <view class="section" v-if="hotJobs.length > 0">
      <view class="section-header">
        <text class="section-title">热门职位</text>
        <text class="section-more" @click="goToJobs">查看更多 ></text>
      </view>
      <view class="job-list">
        <view class="job-card" v-for="job in hotJobs" :key="job.id" @click="goToJobDetail(job.id)">
          <view class="job-header">
            <text class="job-title">{{ job.title }}</text>
            <text class="job-salary" v-if="job.salary_min && job.salary_max">
              {{ job.salary_min }}-{{ job.salary_max }}K
            </text>
          </view>
          <view class="job-info">
            <text class="job-company">{{ job.company_name }}</text>
            <text class="job-location">{{ job.location }}</text>
          </view>
          <view class="job-tags" v-if="job.tags">
            <text class="job-tag" v-for="(tag, idx) in job.tags.slice(0, 3)" :key="idx">{{ tag }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 推荐课程 -->
    <view class="section" v-if="recommendCourses.length > 0">
      <view class="section-header">
        <text class="section-title">推荐课程</text>
        <text class="section-more" @click="goToCourses">查看更多 ></text>
      </view>
      <scroll-view class="course-scroll" scroll-x>
        <view class="course-list">
          <view class="course-card" v-for="course in recommendCourses" :key="course.id" @click="goToCourseDetail(course.id)">
            <view class="course-cover">
              <image :src="getCoverImage(course.cover_image)" mode="aspectFill" class="cover-img" />
              <view class="course-price" v-if="course.price > 0">
                ¥{{ course.price }}
              </view>
              <view class="course-price free" v-else>
                免费
              </view>
            </view>
            <view class="course-info">
              <text class="course-name">{{ course.title }}</text>
              <view class="course-meta">
                <text class="course-instructor">{{ course.instructor || course.provider }}</text>
                <text class="course-enrolled">{{ course.enrolled_count || 0 }}人学习</text>
              </view>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi } from '@/api/jobs'
import { trainingApi } from '@/api/training'

// 轮播图数据
const banners = ref([
  {
    title: '春季校园招聘',
    desc: '千企万岗，职等你来',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    title: '精品课程特惠',
    desc: '限时优惠，助力职业成长',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    title: '考证信息更新',
    desc: '最新考试资讯，不错过报名时间',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  }
])

// 热门职位
const hotJobs = ref([])

// 推荐课程
const recommendCourses = ref([])

// 获取图片
const getCoverImage = (image) => {
  if (!image) return ''
  if (image.startsWith('http')) return image
  return 'http://localhost:5000' + image
}

// 页面跳转
const goToSearch = () => {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

const goToJobs = () => {
  uni.switchTab({ url: '/pages/jobs/list' })
}

const goToCourses = () => {
  uni.switchTab({ url: '/pages/training/courses' })
}

const goToMaterials = () => {
  uni.navigateTo({ url: '/pages/training/materials' })
}

const goToCertifications = () => {
  uni.navigateTo({ url: '/pages/training/certifications' })
}

const goToSocial = () => {
  uni.switchTab({ url: '/pages/social/feed' })
}

const goToFlea = () => {
  uni.navigateTo({ url: '/pages/flea/market' })
}

const goToCampusTalks = () => {
  uni.showToast({ title: '校园宣讲功能开发中', icon: 'none' })
}

const goToInterviews = () => {
  uni.showToast({ title: '面试经验功能开发中', icon: 'none' })
}

const goToJobDetail = (jobId) => {
  uni.navigateTo({ url: `/pages/jobs/detail?id=${jobId}` })
}

const goToCourseDetail = (courseId) => {
  uni.navigateTo({ url: `/pages/training/course-detail?id=${courseId}` })
}

// 获取数据
const fetchHotJobs = async () => {
  try {
    const res = await jobsApi.getJobs({ page: 1, per_page: 3 })
    const data = res.data || res
    hotJobs.value = data.items || data || []
  } catch (error) {
    console.log('获取热门职位失败:', error)
  }
}

const fetchRecommendCourses = async () => {
  try {
    const res = await trainingApi.getCourses({ page: 1, per_page: 6 })
    const data = res.data || res
    recommendCourses.value = data.items || data || []
  } catch (error) {
    console.log('获取推荐课程失败:', error)
  }
}

onMounted(() => {
  fetchHotJobs()
  fetchRecommendCourses()
})
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 120rpx;
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

// 轮播图
.banner-section {
  padding: 20rpx;
}

.banner-swiper {
  height: 300rpx;
  border-radius: 16rpx;
  overflow: hidden;
}

.banner-item {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  border-radius: 16rpx;
}

.banner-title {
  font-size: 40rpx;
  font-weight: bold;
  margin-bottom: 12rpx;
}

.banner-desc {
  font-size: 26rpx;
  opacity: 0.9;
}

// 功能入口
.entry-section {
  background-color: #fff;
  margin: 0 20rpx 20rpx;
  border-radius: 16rpx;
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.entry-grid {
  display: flex;
  flex-wrap: wrap;
}

.entry-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30rpx;
}

.entry-icon {
  width: 96rpx;
  height: 96rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12rpx;
}

.icon-text {
  font-size: 48rpx;
}

.job-icon { background-color: #ecf5ff; }
.course-icon { background-color: #fdf6ec; }
.material-icon { background-color: #f0f9eb; }
.cert-icon { background-color: #fef0f0; }
.social-icon { background-color: #f4f4f5; }
.flea-icon { background-color: #fff0e6; }
.talk-icon { background-color: #eef5ff; }
.interview-icon { background-color: #fff0f6; }

.entry-text {
  font-size: 24rpx;
  color: #606266;
}

// 通用区块
.section {
  background-color: #fff;
  margin: 0 20rpx 20rpx;
  border-radius: 16rpx;
  padding: 30rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.section-more {
  font-size: 26rpx;
  color: #409eff;
}

// 职位列表
.job-list {
  border-top: 1rpx solid #f0f0f0;
}

.job-card {
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
  
  &:last-child {
    border-bottom: none;
  }
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.job-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.job-salary {
  font-size: 30rpx;
  font-weight: bold;
  color: #f56c6c;
}

.job-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.job-company {
  font-size: 26rpx;
  color: #606266;
}

.job-location {
  font-size: 24rpx;
  color: #909399;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.job-tag {
  font-size: 22rpx;
  color: #909399;
  background-color: #f5f7fa;
  padding: 6rpx 16rpx;
  border-radius: 4rpx;
}

// 课程滚动
.course-scroll {
  white-space: nowrap;
}

.course-list {
  display: inline-flex;
  gap: 20rpx;
}

.course-card {
  width: 280rpx;
  flex-shrink: 0;
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.course-cover {
  position: relative;
  width: 100%;
  height: 180rpx;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.course-price {
  position: absolute;
  bottom: 8rpx;
  left: 8rpx;
  background-color: rgba(245, 108, 108, 0.9);
  color: #fff;
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  
  &.free {
    background-color: rgba(103, 194, 58, 0.9);
  }
}

.course-info {
  padding: 16rpx;
}

.course-name {
  font-size: 26rpx;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 8rpx;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-instructor {
  font-size: 22rpx;
  color: #909399;
  max-width: 140rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-enrolled {
  font-size: 22rpx;
  color: #c0c4cc;
}
</style>
