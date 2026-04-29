<template>
  <div class="company-courses">
    <div class="page-header">
      <h2>课程管理</h2>
      <el-button type="primary" @click="goToCreate">
        <el-icon><Plus /></el-icon>
        发布课程
      </el-button>
    </div>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" label-position="right">
        <el-form-item label="课程状态">
          <el-select v-model="filterForm.status" clearable placeholder="全部状态" @change="handleFilterChange">
            <el-option label="报名中" value="active" />
            <el-option label="已结束" value="ended" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程分类">
          <el-select v-model="filterForm.category" clearable placeholder="全部分类" @change="handleFilterChange">
            <el-option label="编程开发" value="programming" />
            <el-option label="语言学习" value="language" />
            <el-option label="考试考证" value="exam_prep" />
            <el-option label="职业技能" value="career" />
            <el-option label="设计创意" value="design" />
            <el-option label="数据科学" value="data" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 课程列表 -->
    <el-card>
      <!-- 空状态引导 -->
      <el-empty v-if="!loading && courses.length === 0" description="暂无课程">
        <template #description>
          <p>您还没有发布任何课程</p>
          <p style="color: #999; font-size: 14px; margin-top: 10px;">点击右上角"发布课程"按钮开始</p>
        </template>
        <el-button type="primary" @click="goToCreate">立即发布课程</el-button>
      </el-empty>
      
      <el-table v-else :data="courses" v-loading="loading" style="width: 100%">
        <el-table-column prop="title" label="课程名称" min-width="200">
          <template #default="{ row }">
            <div class="course-cell" @click="goToDetail(row.id)">
              <div class="course-cover-small">
                <img 
                  :src="getCoverImage(row.cover_image)" 
                  :alt="row.title"
                  class="cover-img"
                />
              </div>
              <div class="course-info-cell">
                <span class="course-title">{{ row.title }}</span>
                <span class="course-meta-small" v-if="row.instructor">
                  讲师：{{ row.instructor }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getCategoryName(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="价格" width="120">
          <template #default="{ row }">
            <span v-if="row.price > 0" class="price-text">¥{{ row.price }}</span>
            <span v-else class="free-text">免费</span>
          </template>
        </el-table-column>
        <el-table-column prop="enrolled_count" label="报名人数" width="100" align="center">
          <template #default="{ row }">
            <span class="enroll-count">{{ row.enrolled_count || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)" size="small">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToEdit(row.id)">编辑</el-button>
            <el-button 
              link 
              :type="row.status === 'active' ? 'warning' : 'success'" 
              @click="toggleStatus(row)"
              :disabled="row.status === 'cancelled'"
            >
              {{ row.status === 'active' ? '下架' : '上架' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="courses.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="perPage"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchCourses"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminCourses, updateCourse, deleteCourse } from '@/api/training'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()

const API_BASE_URL = 'http://localhost:5000'

const courses = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(10)
const total = ref(0)

const filterForm = reactive({
  status: '',
  category: ''
})

// 分类映射
const categoryMap = {
  programming: '编程开发',
  language: '语言学习',
  exam_prep: '考试考证',
  career: '职业技能',
  design: '设计创意',
  data: '数据科学'
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

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

// 获取课程列表
const fetchCourses = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      per_page: perPage.value
    }
    if (filterForm.status) {
      params.status = filterForm.status
    }
    if (filterForm.category) {
      params.category = filterForm.category
    }
    
    const res = await getAdminCourses(params)
    const data = res.data || res
    courses.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取课程失败', error)
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  page.value = 1
  fetchCourses()
}

// 跳转到创建课程
const goToCreate = () => {
  router.push('/admin/courses/create')
}

// 跳转到编辑课程
const goToEdit = (id) => {
  router.push(`/admin/courses/edit/${id}`)
}

// 跳转到课程详情
const goToDetail = (id) => {
  router.push(`/training/courses/${id}`)
}

// 上下架课程
const toggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'ended' : 'active'
  const actionText = newStatus === 'active' ? '上架' : '下架'
  
  try {
    await ElMessageBox.confirm(`确定要${actionText}该课程吗？`, '确认操作', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateCourse(row.id, { status: newStatus })
    row.status = newStatus
    ElMessage.success(`课程已${actionText}`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败，请重试')
    }
  }
}

// 删除课程
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个课程吗？删除后不可恢复！', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteCourse(row.id)
    ElMessage.success('删除成功')
    fetchCourses()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.company-courses {
  padding-top: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 22px;
  color: #333;
}

.filter-card {
  margin-bottom: 20px;
}

.course-cell {
  display: flex;
  gap: 12px;
  align-items: center;
  cursor: pointer;
}

.course-cover-small {
  width: 80px;
  height: 50px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.course-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-meta-small {
  font-size: 12px;
  color: #909399;
}

.price-text {
  font-size: 14px;
  font-weight: bold;
  color: #f56c6c;
}

.free-text {
  font-size: 14px;
  font-weight: bold;
  color: #67c23a;
}

.enroll-count {
  font-size: 14px;
  color: #409eff;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
