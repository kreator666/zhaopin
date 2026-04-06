<template>
  <div class="my-jobs-page">
    <Navbar />
    
    <div class="container" style="padding-top: 80px;">
      <el-card>
        <template #header>
          <div class="card-header">
            <h2>我的职位</h2>
            <el-button type="primary" @click="goToPublish">
              <el-icon><Plus /></el-icon>
              发布职位
            </el-button>
          </div>
        </template>
        
        <el-table :data="jobs" v-loading="loading" style="width: 100%">
          <el-table-column prop="title" label="职位名称" min-width="180">
            <template #default="{ row }">
              <el-link type="primary" @click="viewJob(row.id)">{{ row.title }}</el-link>
            </template>
          </el-table-column>
          
          <el-table-column label="薪资范围" width="150">
            <template #default="{ row }">
              {{ row.salary_min || 0 }}k - {{ row.salary_max || 0 }}k
            </template>
          </el-table-column>
          
          <el-table-column prop="location" label="工作地点" width="120" />
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'info'">
                {{ row.status === 'active' ? '招聘中' : '已关闭' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="发布时间" width="180">
            <template #default="{ row }">
              {{ formatTime(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button link type="primary" @click="editJob(row.id)">编辑</el-button>
              <el-button link type="danger" @click="deleteJob(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="total > pageSize">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :total="total"
            layout="prev, pager, next"
            @change="fetchJobs"
          />
        </div>
        
        <el-empty v-if="!loading && jobs.length === 0" description="暂无发布的职位" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { jobsApi } from '@/api/jobs'

const router = useRouter()

const loading = ref(false)
const jobs = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await jobsApi.getMyJobs({
      page: page.value,
      per_page: pageSize.value
    })
    const data = res.data || res
    jobs.value = data.items || []
    total.value = data.total || 0
  } catch (err) {
    console.error('获取职位列表失败:', err)
    ElMessage.error('获取职位列表失败')
  } finally {
    loading.value = false
  }
}

const goToPublish = () => {
  router.push('/jobs/publish')
}

const viewJob = (id) => {
  router.push(`/jobs/${id}`)
}

const editJob = (id) => {
  router.push(`/jobs/edit/${id}`)
}

const deleteJob = async (job) => {
  try {
    await ElMessageBox.confirm(
      `确定删除职位"${job.title}"？此操作不可恢复`,
      '确认删除',
      { type: 'warning' }
    )
    
    await jobsApi.delete(job.id)
    ElMessage.success('删除成功')
    fetchJobs()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.my-jobs-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
