<template>
  <div class="company-certs">
    <div class="page-header">
      <h2>考证信息管理</h2>
      <el-button type="primary" @click="goToCreate">
        <el-icon><Plus /></el-icon>
        发布考证信息
      </el-button>
    </div>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" label-position="right">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" clearable placeholder="全部状态" @change="handleFilterChange">
            <el-option label="即将开始" value="upcoming" />
            <el-option label="报名中" value="ongoing" />
            <el-option label="已结束" value="ended" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filterForm.category" clearable placeholder="全部分类" @change="handleFilterChange">
            <el-option label="语言考试" value="language" />
            <el-option label="计算机等级" value="computer" />
            <el-option label="职业资格" value="professional" />
            <el-option label="金融财会" value="finance" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 列表 -->
    <el-card>
      <el-empty v-if="!loading && certifications.length === 0" description="暂无考证信息">
        <template #description>
          <p>您还没有发布任何考证信息</p>
          <p style="color: #999; font-size: 14px; margin-top: 10px;">点击右上角"发布考证信息"按钮开始</p>
        </template>
        <el-button type="primary" @click="goToCreate">立即发布</el-button>
      </el-empty>
      
      <el-table v-else :data="certifications" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="考证名称" min-width="200">
          <template #default="{ row }">
            <div class="cert-cell" @click="goToDetail(row.id)">
              <span class="cert-title">{{ row.name }}</span>
              <span class="cert-organizer" v-if="row.organizer">
                主办：{{ row.organizer }}
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getCategoryName(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="报名时间" width="220">
          <template #default="{ row }">
            <div class="time-info">
              <span v-if="row.registration_start">{{ row.registration_start }} ~ {{ row.registration_end || '-' }}</span>
              <span v-else class="no-info">待定</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考试时间" width="120">
          <template #default="{ row }">
            <span v-if="row.exam_date">{{ row.exam_date }}</span>
            <span v-else class="no-info">待定</span>
          </template>
        </el-table-column>
        <el-table-column label="费用" width="100">
          <template #default="{ row }">
            <span v-if="row.fee !== null && row.fee !== undefined">
              {{ row.fee > 0 ? '¥' + row.fee : '免费' }}
            </span>
            <span v-else class="no-info">待定</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)" size="small">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发布时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToEdit(row.id)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="certifications.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="perPage"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchCertifications"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminCertifications, deleteCertification } from '@/api/training'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()

const certifications = ref([])
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

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
}

// 获取状态名称
const getStatusName = (status) => {
  return statusMap[status]?.name || status
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  return statusMap[status]?.type || 'info'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

// 获取列表
const fetchCertifications = async () => {
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
    
    const res = await getAdminCertifications(params)
    const data = res.data || res
    certifications.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取考证信息失败', error)
    ElMessage.error('获取考证信息失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  page.value = 1
  fetchCertifications()
}

// 跳转创建
const goToCreate = () => {
  router.push('/company/certifications/create')
}

// 跳转编辑
const goToEdit = (id) => {
  router.push(`/company/certifications/edit/${id}`)
}

// 跳转详情（学生端）
const goToDetail = (id) => {
  router.push(`/training/certifications/${id}`)
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个考证信息吗？删除后不可恢复！', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteCertification(row.id)
    ElMessage.success('删除成功')
    fetchCertifications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

onMounted(() => {
  fetchCertifications()
})
</script>

<style scoped>
.company-certs {
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

.cert-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}

.cert-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.cert-organizer {
  font-size: 12px;
  color: #909399;
}

.time-info {
  font-size: 13px;
  color: #606266;
}

.no-info {
  font-size: 13px;
  color: #c0c4cc;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
