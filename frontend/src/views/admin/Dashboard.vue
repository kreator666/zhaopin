<template>
  <div class="admin-dashboard">
    <h2 class="page-title">运营概览</h2>
    
    <!-- 欢迎卡片 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <div class="welcome-info">
          <h3>欢迎回来，{{ userStore.userInfo?.username }}</h3>
          <p>今天是 {{ currentDate }}，祝您工作愉快！</p>
        </div>
        <div class="welcome-icon">
          <el-icon :size="80"><Promotion /></el-icon>
        </div>
      </div>
    </el-card>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon blue">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalCourses }}</div>
            <div class="stat-label">精品课程</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon green">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalCertifications }}</div>
            <div class="stat-label">考证信息</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon orange">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalEnrollments }}</div>
            <div class="stat-label">课程报名</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon purple">
            <el-icon><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.activeCourses }}</div>
            <div class="stat-label">进行中课程</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快速操作 -->
    <el-card class="quick-actions">
      <template #header>
        <span>快速操作</span>
      </template>
      <div class="action-list">
        <div class="action-item" @click="goToCreateCourse">
          <div class="action-icon blue">
            <el-icon><Plus /></el-icon>
          </div>
          <div class="action-info">
            <h4>发布新课程</h4>
            <p>创建新的精品课程，供学生报名学习</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="action-item" @click="goToCreateCertification">
          <div class="action-icon green">
            <el-icon><Plus /></el-icon>
          </div>
          <div class="action-info">
            <h4>发布考证信息</h4>
            <p>发布最新的考证资讯，帮助学生备考</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="action-item" @click="goToCourses">
          <div class="action-icon orange">
            <el-icon><Management /></el-icon>
          </div>
          <div class="action-info">
            <h4>管理课程</h4>
            <p>查看、编辑、上下架已发布的课程</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="action-item" @click="goToCertifications">
          <div class="action-icon purple">
            <el-icon><Management /></el-icon>
          </div>
          <div class="action-info">
            <h4>管理考证信息</h4>
            <p>查看、编辑、删除已发布的考证信息</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>
    
    <!-- 最近课程 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="recent-card">
          <template #header>
            <div class="card-header">
              <span>最近发布的课程</span>
              <el-link type="primary" @click="goToCourses">查看全部</el-link>
            </div>
          </template>
          <div v-if="recentCourses.length === 0" class="empty-list">
            暂无课程，快去发布吧！
          </div>
          <el-table v-else :data="recentCourses" style="width: 100%" size="small">
            <el-table-column prop="title" label="课程名称" min-width="180" show-overflow-tooltip />
            <el-table-column prop="category" label="分类" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ getCategoryName(row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
                  {{ row.status === 'active' ? '报名中' : '已结束' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="recent-card">
          <template #header>
            <div class="card-header">
              <span>最近发布的考证信息</span>
              <el-link type="primary" @click="goToCertifications">查看全部</el-link>
            </div>
          </template>
          <div v-if="recentCertifications.length === 0" class="empty-list">
            暂无考证信息，快去发布吧！
          </div>
          <el-table v-else :data="recentCertifications" style="width: 100%" size="small">
            <el-table-column prop="name" label="考证名称" min-width="180" show-overflow-tooltip />
            <el-table-column prop="category" label="分类" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ getCertCategoryName(row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)" size="small">
                  {{ getStatusName(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getAdminCourses, getAdminCertifications } from '@/api/training'
import { Promotion, VideoPlay, Document, User, Star, Plus, ArrowRight, Management } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  })
})

const stats = ref({
  totalCourses: 0,
  totalCertifications: 0,
  totalEnrollments: 0,
  activeCourses: 0
})

const recentCourses = ref([])
const recentCertifications = ref([])

// 课程分类映射
const courseCategoryMap = {
  programming: '编程开发',
  language: '语言学习',
  exam_prep: '考试考证',
  career: '职业技能',
  design: '设计创意',
  data: '数据科学'
}

// 考证分类映射
const certCategoryMap = {
  language: '语言考试',
  computer: '计算机等级',
  professional: '职业资格',
  finance: '金融财会',
  other: '其他'
}

// 状态映射
const statusMap = {
  upcoming: { name: '即将开始', type: 'warning' },
  ongoing: { name: '报名中', type: 'success' },
  ended: { name: '已结束', type: 'info' }
}

const getCategoryName = (category) => {
  return courseCategoryMap[category] || '其他'
}

const getCertCategoryName = (category) => {
  return certCategoryMap[category] || '其他'
}

const getStatusName = (status) => {
  return statusMap[status]?.name || status
}

const getStatusTagType = (status) => {
  return statusMap[status]?.type || 'info'
}

const fetchData = async () => {
  try {
    // 获取课程数据
    const coursesRes = await getAdminCourses({ per_page: 100 })
    const coursesData = coursesRes.data || coursesRes
    const courses = coursesData.items || []
    
    stats.value.totalCourses = courses.length
    stats.value.activeCourses = courses.filter(c => c.status === 'active').length
    recentCourses.value = courses.slice(0, 5)
    
    // 获取考证信息数据
    const certsRes = await getAdminCertifications({ per_page: 100 })
    const certsData = certsRes.data || certsRes
    const certs = certsData.items || []
    
    stats.value.totalCertifications = certs.length
    recentCertifications.value = certs.slice(0, 5)
    
    // 统计报名人数（简化）
    stats.value.totalEnrollments = courses.reduce((sum, c) => sum + (c.enrolled_count || 0), 0)
  } catch (error) {
    console.error('获取数据失败', error)
  }
}

const goToCreateCourse = () => {
  router.push('/admin/courses/create')
}

const goToCreateCertification = () => {
  router.push('/admin/certifications/create')
}

const goToCourses = () => {
  router.push('/admin/courses')
}

const goToCertifications = () => {
  router.push('/admin/certifications')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.admin-dashboard {
  padding-top: 0;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #333;
}

.welcome-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.welcome-card :deep(.el-card__body) {
  padding: 24px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.welcome-info h3 {
  margin: 0 0 10px 0;
  font-size: 20px;
}

.welcome-info p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.welcome-icon {
  opacity: 0.3;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-right: 15px;
}

.stat-icon.blue {
  background: #ecf5ff;
  color: #409EFF;
}

.stat-icon.green {
  background: #f0f9eb;
  color: #67c23a;
}

.stat-icon.orange {
  background: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.purple {
  background: #f5f0ff;
  color: #9254de;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.quick-actions {
  margin-bottom: 20px;
}

.action-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.action-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background: #ecf5ff;
  transform: translateX(5px);
}

.action-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background: #409EFF;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.action-icon.blue {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
}

.action-icon.green {
  background: linear-gradient(135deg, #67C23A 0%, #909399 100%);
}

.action-icon.orange {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
}

.action-icon.purple {
  background: linear-gradient(135deg, #9254de 0%, #409EFF 100%);
}

.action-info {
  flex: 1;
}

.action-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.action-info p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.action-arrow {
  font-size: 20px;
  color: #c0c4cc;
}

.recent-card {
  min-height: 300px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-list {
  text-align: center;
  padding: 40px 0;
  color: #909399;
}
</style>
