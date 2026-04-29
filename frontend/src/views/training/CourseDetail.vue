<template>
  <div class="course-detail-page">
    <Navbar />
    
    <div class="main-content" v-loading="loading">
      <div class="container" v-if="course">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item :to="{ path: '/training' }">培训学习</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/training/courses' }">精品课程</el-breadcrumb-item>
          <el-breadcrumb-item>{{ course.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        
        <!-- 课程头部 -->
        <div class="course-header">
          <div class="course-cover">
            <img 
              :src="getCoverImage(course.cover_image)" 
              :alt="course.title"
              class="cover-img"
            />
            <div class="course-badges">
              <el-tag v-if="course.is_online" type="primary" effect="dark">线上课程</el-tag>
              <el-tag v-else type="warning" effect="dark">线下课程</el-tag>
              <el-tag v-if="course.price === 0" type="success" effect="dark">免费</el-tag>
            </div>
          </div>
          
          <div class="course-info">
            <h1 class="course-title">{{ course.title }}</h1>
            
            <div class="course-meta-top">
              <span class="meta-item" v-if="course.instructor">
                <el-icon><User /></el-icon>
                讲师：{{ course.instructor }}
              </span>
              <span class="meta-item" v-if="course.provider">
                <el-icon><OfficeBuilding /></el-icon>
                机构：{{ course.provider }}
              </span>
              <span class="meta-item" v-if="course.duration">
                <el-icon><Clock /></el-icon>
                时长：{{ course.duration }}
              </span>
              <span class="meta-item" v-if="course.level">
                <el-tag :type="getLevelTagType(course.level)" size="small">
                  {{ getLevelName(course.level) }}
                </el-tag>
              </span>
            </div>
            
            <div class="course-stats-row">
              <div class="stat-item">
                <span class="stat-value">{{ course.enrolled_count || 0 }}</span>
                <span class="stat-label">人学习</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ course.rating || 5.0 }}</span>
                <span class="stat-label">评分</span>
              </div>
              <div class="stat-item" v-if="course.review_count">
                <span class="stat-value">{{ course.review_count }}</span>
                <span class="stat-label">评价</span>
              </div>
            </div>
            
            <div class="course-price-section">
              <div class="price-display">
                <span class="current-price" v-if="course.price > 0">
                  ¥{{ course.price }}
                </span>
                <span class="current-price free" v-else>
                  免费
                </span>
                <span class="original-price" v-if="course.original_price && course.original_price > course.price">
                  原价 ¥{{ course.original_price }}
                </span>
              </div>
              
              <div class="action-buttons">
                <template v-if="userStore.isLoggedIn">
                  <el-button 
                    v-if="!isEnrolled && course.status === 'active'"
                    type="primary" 
                    size="large" 
                    :loading="enrolling"
                    @click="handleEnroll"
                  >
                    <el-icon><Plus /></el-icon>
                    立即报名
                  </el-button>
                  <el-button 
                    v-else-if="isEnrolled"
                    type="success" 
                    size="large"
                    disabled
                  >
                    <el-icon><Check /></el-icon>
                    已报名
                  </el-button>
                  <el-button 
                    v-else-if="course.status === 'ended'"
                    size="large"
                    disabled
                  >
                    课程已结束
                  </el-button>
                  <el-button 
                    v-else-if="course.status === 'cancelled'"
                    size="large"
                    disabled
                  >
                    课程已取消
                  </el-button>
                </template>
                <el-button 
                  v-else
                  type="primary" 
                  size="large"
                  @click="$router.push('/login')"
                >
                  登录报名
                </el-button>
                
                <el-button size="large" @click="$router.back()">
                  <el-icon><ArrowLeft /></el-icon>
                  返回
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 课程详情内容 -->
        <div class="course-content">
          <div class="content-left">
            <!-- 课程描述 -->
            <el-card class="content-card">
              <template #header>
                <h3 class="card-title">
                  <el-icon><Document /></el-icon>
                  课程简介
                </h3>
              </template>
              <div class="description-content">
                <p v-if="course.description">{{ course.description }}</p>
                <p v-else class="no-content">暂无课程简介</p>
              </div>
            </el-card>
            
            <!-- 课程信息 -->
            <el-card class="content-card">
              <template #header>
                <h3 class="card-title">
                  <el-icon><InfoFilled /></el-icon>
                  课程详情
                </h3>
              </template>
              <el-descriptions :column="2" border>
                <el-descriptions-item label="课程分类">
                  <el-tag size="small">{{ getCategoryName(course.category) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="课程级别">
                  <el-tag :type="getLevelTagType(course.level)" size="small">
                    {{ getLevelName(course.level) }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="授课形式">
                  {{ course.is_online ? '线上课程' : '线下课程' }}
                </el-descriptions-item>
                <el-descriptions-item label="课程时长" v-if="course.duration">
                  {{ course.duration }}
                </el-descriptions-item>
                <el-descriptions-item label="开课日期" v-if="course.start_date">
                  {{ course.start_date }}
                </el-descriptions-item>
                <el-descriptions-item label="结束日期" v-if="course.end_date">
                  {{ course.end_date }}
                </el-descriptions-item>
                <el-descriptions-item label="授课地点" v-if="!course.is_online && course.location">
                  {{ course.location }}
                </el-descriptions-item>
                <el-descriptions-item label="课程状态">
                  <el-tag :type="getStatusTagType(course.status)" size="small">
                    {{ getStatusName(course.status) }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
          
          <!-- 侧边栏 -->
          <div class="content-right">
            <!-- 讲师信息 -->
            <el-card class="sidebar-card" v-if="course.instructor">
              <template #header>
                <h4 class="sidebar-title">讲师信息</h4>
              </template>
              <div class="instructor-info">
                <el-avatar :size="56" class="instructor-avatar">
                  {{ course.instructor.charAt(0) }}
                </el-avatar>
                <div class="instructor-detail">
                  <span class="instructor-name">{{ course.instructor }}</span>
                  <span class="instructor-desc" v-if="course.provider">
                    来自 {{ course.provider }}
                  </span>
                </div>
              </div>
            </el-card>
            
            <!-- 学习人数排行 -->
            <el-card class="sidebar-card">
              <template #header>
                <h4 class="sidebar-title">热门课程</h4>
              </template>
              <div class="hot-courses">
                <el-empty v-if="hotCourses.length === 0" description="暂无热门课程" :image-size="60" />
                <div 
                  v-for="(course, index) in hotCourses" 
                  :key="course.id" 
                  class="hot-course-item"
                  @click="goToDetail(course.id)"
                >
                  <span class="rank-number" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
                  <div class="hot-course-info">
                    <span class="hot-course-title">{{ course.title }}</span>
                    <span class="hot-course-meta">
                      {{ course.enrolled_count || 0 }}人学习
                    </span>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
      
      <!-- 错误状态 -->
      <div class="error-container" v-else-if="!loading">
        <el-empty description="课程不存在或已被删除" />
        <el-button type="primary" @click="$router.push('/training/courses')">返回课程列表</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getCourse, enrollCourse, checkEnrollment, getCourses } from '@/api/training'
import {
  User, OfficeBuilding, Clock, Plus, Check, ArrowLeft,
  Document, InfoFilled
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(true)
const course = ref(null)
const isEnrolled = ref(false)
const enrolling = ref(false)
const hotCourses = ref([])

// 分类映射
const categoryMap = {
  programming: '编程开发',
  language: '语言学习',
  exam_prep: '考试考证',
  career: '职业技能',
  design: '设计创意',
  data: '数据科学'
}

// 难度映射
const levelMap = {
  beginner: { name: '入门', type: 'success' },
  intermediate: { name: '进阶', type: 'warning' },
  advanced: { name: '高级', type: 'danger' }
}

// 状态映射
const statusMap = {
  active: { name: '报名中', type: 'primary' },
  ended: { name: '已结束', type: 'info' },
  cancelled: { name: '已取消', type: 'danger' }
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || category
}

// 获取难度名称
const getLevelName = (level) => {
  return levelMap[level]?.name || level
}

// 获取难度标签类型
const getLevelTagType = (level) => {
  return levelMap[level]?.type || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  return statusMap[status]?.name || status
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  return statusMap[status]?.type || 'info'
}

// 获取封面图片
const getCoverImage = (coverImage) => {
  if (!coverImage) {
    return 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=online%20course%20education%20learning%20technology%20modern%20design&image_size=landscape_16_9'
  }
  if (coverImage.startsWith('http')) {
    return coverImage
  }
  return `${API_BASE_URL}${coverImage}`
}

// 获取课程详情
const fetchCourseDetail = async () => {
  const courseId = route.params.id
  if (!courseId) {
    loading.value = false
    return
  }
  
  loading.value = true
  try {
    const res = await getCourse(courseId)
    const data = res.data || res
    course.value = data
    
    // 如果已登录，检查是否已报名
    if (userStore.isLoggedIn) {
      const enrollRes = await checkEnrollment(courseId)
      isEnrolled.value = enrollRes.data?.enrolled || false
    }
  } catch (error) {
    console.error('获取课程详情失败', error)
    ElMessage.error('获取课程详情失败')
  } finally {
    loading.value = false
  }
}

// 获取热门课程
const fetchHotCourses = async () => {
  try {
    const res = await getCourses({
      page: 1,
      per_page: 5
    })
    const data = res.data || res
    hotCourses.value = (data.items || []).filter(c => c.id !== course.value?.id)
  } catch (error) {
    console.error('获取热门课程失败', error)
  }
}

// 报名课程
const handleEnroll = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  if (!course.value) return
  
  enrolling.value = true
  try {
    await enrollCourse(course.value.id)
    isEnrolled.value = true
    course.value.enrolled_count = (course.value.enrolled_count || 0) + 1
    ElMessage.success('报名成功！')
  } catch (error) {
    console.error('报名失败', error)
    const errMsg = error.response?.data?.error || '报名失败，请重试'
    ElMessage.error(errMsg)
  } finally {
    enrolling.value = false
  }
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/training/courses/${id}`)
}

onMounted(async () => {
  await fetchCourseDetail()
  fetchHotCourses()
})
</script>

<style scoped>
.course-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding: 100px 0 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.course-header {
  display: flex;
  gap: 30px;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.course-cover {
  width: 440px;
  flex-shrink: 0;
  position: relative;
}

.cover-img {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 8px;
}

.course-badges {
  position: absolute;
  top: 16px;
  left: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.course-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.course-title {
  font-size: 24px;
  color: #333;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.course-meta-top {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #666;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.course-stats-row {
  display: flex;
  gap: 40px;
  padding: 16px 0;
  margin-bottom: 20px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.course-stats-row .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.course-stats-row .stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.course-stats-row .stat-label {
  font-size: 13px;
  color: #909399;
}

.course-price-section {
  margin-top: auto;
}

.price-display {
  margin-bottom: 16px;
}

.current-price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
}

.current-price.free {
  color: #67c23a;
}

.original-price {
  font-size: 16px;
  color: #c0c4cc;
  text-decoration: line-through;
  margin-left: 12px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.course-content {
  display: flex;
  gap: 24px;
}

.content-left {
  flex: 1;
  min-width: 0;
}

.content-card {
  margin-bottom: 20px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 16px;
  color: #333;
}

.description-content {
  line-height: 1.8;
  color: #666;
}

.description-content p {
  margin: 0;
  white-space: pre-wrap;
}

.no-content {
  color: #909399;
  text-align: center;
}

.content-right {
  width: 300px;
  flex-shrink: 0;
}

.sidebar-card {
  margin-bottom: 20px;
}

.sidebar-title {
  margin: 0;
  font-size: 15px;
  color: #333;
}

.instructor-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.instructor-avatar {
  background: linear-gradient(135deg, #409eff, #67c23a);
  color: #fff;
  font-size: 20px;
  font-weight: bold;
}

.instructor-detail {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.instructor-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.instructor-desc {
  font-size: 13px;
  color: #909399;
}

.hot-courses {
  margin: -8px 0;
}

.hot-course-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.hot-course-item:last-child {
  border-bottom: none;
}

.hot-course-item:hover {
  background-color: #f5f7fa;
  margin: 0 -12px;
  padding: 12px;
  border-radius: 4px;
}

.rank-number {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  border-radius: 4px;
  flex-shrink: 0;
}

.rank-1 {
  background: #f56c6c;
  color: #fff;
}

.rank-2 {
  background: #e6a23c;
  color: #fff;
}

.rank-3 {
  background: #409eff;
  color: #fff;
}

.rank-number:not(.rank-1):not(.rank-2):not(.rank-3) {
  background: #f0f0f0;
  color: #909399;
}

.hot-course-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.hot-course-title {
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hot-course-meta {
  font-size: 12px;
  color: #909399;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
}

@media (max-width: 992px) {
  .course-header {
    flex-direction: column;
  }
  
  .course-cover {
    width: 100%;
  }
  
  .course-content {
    flex-direction: column;
  }
  
  .content-right {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .course-header {
    padding: 16px;
  }
  
  .cover-img {
    height: 200px;
  }
  
  .course-stats-row {
    gap: 20px;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
}
</style>
