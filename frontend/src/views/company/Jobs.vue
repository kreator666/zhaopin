<template>
  <div>
    <Navbar />
    <div class="company-jobs">
    <div class="page-header">
      <h2>职位管理</h2>
      <el-button type="primary" @click="goToCreate">
        <el-icon><Plus /></el-icon>
        发布职位
      </el-button>
    </div>
    
    <el-card>
      <!-- 空状态引导 -->
      <el-empty v-if="!loading && jobs.length === 0" description="暂无职位">
        <template #description>
          <p>您还没有发布任何职位</p>
          <p style="color: #999; font-size: 14px; margin-top: 10px;">点击右上角"发布职位"按钮开始招聘</p>
        </template>
        <el-button type="primary" @click="goToCreate">立即发布职位</el-button>
      </el-empty>
      
      <el-table v-else :data="jobs" v-loading="loading" style="width: 100%">
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
      
      <div v-if="jobs.length > 0" class="pagination">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { jobsApi } from '@/api/jobs'
import Navbar from '@/components/Navbar.vue'

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
    const data = res.data || res
    jobs.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取职位失败', error)
  } finally {
    loading.value = false
  }
}

const goToCreate = () => {
  router.push('/jobs/publish')
}

const goToEdit = (id) => {
  router.push(`/jobs/edit/${id}`)
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
.company-jobs {
  padding-top: 60px;
}

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
