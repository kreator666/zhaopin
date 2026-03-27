<template>
  <div class="company-jobs">
    <div class="page-header">
      <h2>职位管理</h2>
      <el-button type="primary" @click="goToCreate">
        <el-icon><Plus /></el-icon>
        发布职位
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="jobs" v-loading="loading" style="width: 100%">
        <el-table-column prop="title" label="职位名称" min-width="150" />
        <el-table-column label="薪资范围" width="150">
          <template #default="{ row }">
            {{ formatSalary(row.salary_min, row.salary_max) }}
          </template>
        </el-table-column>
        <el-table-column prop="location" label="工作地点" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '招聘中' : '已下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="浏览量" width="100" align="center">
          <template #default="{ row }">
            {{ row.view_count }}
          </template>
        </el-table-column>
        <el-table-column label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToEdit(row.id)">编辑</el-button>
            <el-button link :type="row.status === 'active' ? 'warning' : 'success'" @click="toggleStatus(row)">
              {{ row.status === 'active' ? '下架' : '上架' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="perPage"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchJobs"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { jobsApi } from '@/api/jobs'

const router = useRouter()

const jobs = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(10)
const total = ref(0)

const formatSalary = (min, max) => {
  if (!min && !max) return '薪资面议'
  return `${min || 0}K - ${max || 0}K`
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await jobsApi.getMyJobs({
      page: page.value,
      per_page: perPage.value
    })
    jobs.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('获取职位失败', error)
  } finally {
    loading.value = false
  }
}

const goToCreate = () => {
  router.push('/company/jobs/create')
}

const goToEdit = (id) => {
  router.push(`/company/jobs/edit/${id}`)
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'inactive' : 'active'
  try {
    await jobsApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 'active' ? '职位已上架' : '职位已下架')
    fetchJobs()
  } catch (error) {
    console.error('操作失败', error)
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个职位吗？删除后不可恢复！', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await jobsApi.delete(id)
    ElMessage.success('删除成功')
    fetchJobs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
    }
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
