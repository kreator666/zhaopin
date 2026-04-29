<template>
  <div class="my-courses-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <!-- 页面头部 -->
        <div class="page-header">
          <div class="header-left">
            <h1>我的课程</h1>
            <p>查看和管理已报名的课程</p>
          </div>
          <el-button type="primary" size="large" @click="$router.push('/training/courses')">
            <el-icon><Plus /></el-icon>
            发现更多课程
          </el-button>
        </div>
        
        <!-- 筛选标签 -->
        <div class="filter-tabs">
          <el-radio-group v-model="currentStatus" size="large" @change="handleStatusChange">
            <el-radio-button value="">全部课程</el-radio-button>
            <el-radio-button value="enrolled">学习中</el-radio-button>
            <el-radio-button value="completed">已完成</el-radio-button>
            <el-radio-button value="dropped">已退课</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 课程列表 -->
        <div class="courses-section" v-loading="loading">
          <div v-if="enrollments.length > 0">
            <div 
              v-for="enrollment in enrollments" 
              :key="enrollment.id" 
              class="course-item"
            >
              <div class="course-card" @click="goToDetail(enrollment.course_id)">
                <div class="course-cover">
                  <img 
                    :src="getCoverImage(enrollment.course?.cover_image)" 
                    :alt="enrollment.course?.title"
                    class="cover-img"
                  />
                  <div class="course-status-tag">
                    <el-tag :type="getStatusTagType(enrollment.status)" effect="dark">
                      {{ getStatusName(enrollment.status) }}
                    </el-tag>
                  </div>
                </div>
                
                <div class="course-info">
                  <h3 class="course-title">{{ enrollment.course?.title }}</h3>
                  
                  <div class="course-meta">
                    <span class="meta-item" v-if="enrollment.course?.instructor">
                      <el-icon><User /></el-icon>
                      讲师：{{ enrollment.course?.instructor }}
                    </span>
                    <span class="meta-item" v-if="enrollment.course?.provider">
                      <el-icon><OfficeBuilding /></el-icon>
                      机构：{{ enrollment.course?.provider }}
                    </span>
                    <span class="meta-item" v-if="enrollment.course?.duration">
                      <el-icon><Clock /></el-icon>
                      时长：{{ enrollment.course?.duration }}
                    </span>
                  </div>
                  
                  <div class="course-desc" v-if="enrollment.course?.description">
                    {{ enrollment.course?.description }}
                  </div>
                  
                  <div class="enrollment-info">
                    <span class="enroll-time">
                      报名时间：{{ formatDateTime(enrollment.enrolled_at) }}
                    </span>
                    <span class="complete-time" v-if="enrollment.completed_at">
                      完成时间：{{ formatDateTime(enrollment.completed_at) }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="course-actions">
                <el-button 
                  type="primary" 
                  size="large"
                  @click="goToDetail(enrollment.course_id)"
                >
                  <el-icon><View /></el-icon>
                  继续学习
                </el-button>
                
                <template v-if="enrollment.status === 'enrolled'">
                  <el-button 
                    size="large" 
                    type="danger"
                    @click="handleDropCourse(enrollment)"
                  >
                    <el-icon><Remove /></el-icon>
                    退课
                  </el-button>
                </template>
                
                <template v-if="enrollment.status === 'enrolled'">
                  <el-button 
                    size="large" 
                    type="success"
                    @click="handleCompleteCourse(enrollment)"
                  >
                    <el-icon><Check /></el-icon>
                    标记完成
                  </el-button>
                </template>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-container">
            <el-empty description="暂无已报名的课程" :image-size="120">
              <template #description>
                <p>您还没有报名任何课程</p>
                <p>快去发现适合自己的课程吧！</p>
              </template>
              <el-button type="primary" @click="$router.push('/training/courses')">
                浏览课程
              </el-button>
            </el-empty>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 退课确认对话框 -->
    <el-dialog
      v-model="showDropDialog"
      title="确认退课"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>确定要退选该课程吗？退课后将无法继续学习。</p>
      <template #footer>
        <el-button @click="showDropDialog = false">取消</el-button>
        <el-button type="danger" :loading="submitting" @click="confirmDropCourse">
          确认退课
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { getMyCourses } from '@/api/training'
import {
  Plus, User, OfficeBuilding, Clock, View, Remove, Check
} from '@element-plus/icons-vue'

const router = useRouter()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const enrollments = ref([])
const currentStatus = ref('')
const showDropDialog = ref(false)
const submitting = ref(false)
const currentEnrollment = ref(null)

// 状态映射
const statusMap = {
  enrolled: { name: '学习中', type: 'primary' },
  completed: { name: '已完成', type: 'success' },
  dropped: { name: '已退课', type: 'danger' }
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

// 格式化日期时间
const formatDateTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取我的课程列表
const fetchMyCourses = async () => {
  loading.value = true
  try {
    const params = {}
    if (currentStatus.value) {
      params.status = currentStatus.value
    }
    
    const res = await getMyCourses(params)
    const data = res.data || res
    enrollments.value = data.items || []
  } catch (error) {
    console.error('获取我的课程失败', error)
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

// 状态筛选变化
const handleStatusChange = () => {
  fetchMyCourses()
}

// 跳转到课程详情
const goToDetail = (id) => {
  if (id) {
    router.push(`/training/courses/${id}`)
  }
}

// 退课
const handleDropCourse = (enrollment) => {
  currentEnrollment.value = enrollment
  showDropDialog.value = true
}

// 确认退课
const confirmDropCourse = async () => {
  if (!currentEnrollment.value) return
  
  submitting.value = true
  try {
    // TODO: 调用后端退课接口
    // await dropCourse(currentEnrollment.value.id)
    ElMessage.success('退课成功')
    showDropDialog.value = false
    fetchMyCourses()
  } catch (error) {
    console.error('退课失败', error)
    ElMessage.error('退课失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 标记完成
const handleCompleteCourse = async (enrollment) => {
  try {
    await ElMessageBox.confirm(
      '确定要将该课程标记为已完成吗？',
      '确认完成',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    // TODO: 调用后端标记完成接口
    // await completeCourse(enrollment.id)
    ElMessage.success('已标记为完成')
    fetchMyCourses()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('标记完成失败', error)
      ElMessage.error('操作失败，请重试')
    }
  }
}

onMounted(() => {
  fetchMyCourses()
})
</script>

<style scoped>
.my-courses-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding: 100px 0 40px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #333;
}

.header-left p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.filter-tabs {
  margin-bottom: 24px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.courses-section {
  min-height: 300px;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.course-card {
  display: flex;
  gap: 20px;
  flex: 1;
  cursor: pointer;
  transition: opacity 0.2s;
}

.course-card:hover {
  opacity: 0.8;
}

.course-cover {
  width: 220px;
  flex-shrink: 0;
  position: relative;
}

.cover-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 6px;
}

.course-status-tag {
  position: absolute;
  top: 10px;
  left: 10px;
}

.course-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.course-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 12px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #666;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-desc {
  font-size: 13px;
  color: #909399;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: auto;
}

.enrollment-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  font-size: 13px;
  color: #909399;
}

.course-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: center;
  flex-shrink: 0;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  background: #fff;
  border-radius: 8px;
}

.empty-container :deep(.el-empty__description) {
  text-align: center;
}

.empty-container :deep(.el-empty__description p) {
  margin: 4px 0;
  color: #909399;
}

@media (max-width: 768px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .course-item {
    flex-direction: column;
  }
  
  .course-actions {
    flex-direction: row;
    justify-content: flex-start;
  }
  
  .course-cover {
    width: 160px;
  }
  
  .cover-img {
    height: 100px;
  }
}
</style>
