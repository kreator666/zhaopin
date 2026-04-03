<template>
  <div class="alumni-circle-page">
    <Navbar />
    
    <div class="main-content">
      <!-- 头部区域 -->
      <div class="page-header">
        <div class="container">
          <div class="header-content">
            <div class="school-info">
              <el-icon :size="48" color="#fff"><School /></el-icon>
              <div class="school-text">
                <h1>{{ stats.school_name || '校友圈' }}</h1>
                <p v-if="stats.my_year">{{ stats.my_year }}级 · 找到 {{ stats.total_alumni }} 位校友</p>
                <p v-else>找到 {{ stats.total_alumni }} 位校友</p>
              </div>
            </div>
            <div class="stats-cards">
              <div class="stat-card">
                <span class="stat-num">{{ stats.total_alumni }}</span>
                <span class="stat-label">总校友</span>
              </div>
              <div class="stat-card" v-if="stats.same_year_count > 0">
                <span class="stat-num">{{ stats.same_year_count }}</span>
                <span class="stat-label">同级校友</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="container">
        <div class="content-wrapper">
          <!-- 搜索筛选区 -->
          <el-card class="filter-card" shadow="hover">
            <el-form :model="searchForm" inline>
              <el-form-item label="姓名">
                <el-input 
                  v-model="searchForm.keyword" 
                  placeholder="搜索校友姓名"
                  clearable
                  @keyup.enter="handleSearch"
                  style="width: 180px"
                />
              </el-form-item>
              
              <el-form-item label="性别">
                <el-select v-model="searchForm.gender" placeholder="全部" clearable style="width: 100px">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="入学年">
                <el-select v-model="searchForm.enrollment_year" placeholder="全部" clearable style="width: 120px">
                  <el-option 
                    v-for="year in yearOptions" 
                    :key="year" 
                    :label="year + '年'" 
                    :value="year" 
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleSearch">
                  <el-icon><Search /></el-icon>搜索
                </el-button>
                <el-button text @click="resetSearch">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <!-- 校友列表 -->
          <el-card class="alumni-list-card" shadow="hover" v-loading="loading">
            <template #header>
              <div class="card-header">
                <span>校友列表</span>
                <span class="total-text">共 {{ total }} 人</span>
              </div>
            </template>
            
            <div v-if="alumniList.length > 0" class="alumni-grid">
              <div 
                v-for="alumni in alumniList" 
                :key="alumni.id" 
                class="alumni-item"
                @click="viewProfile(alumni.id)"
              >
                <el-avatar 
                  :size="64" 
                  :src="getFullImageUrl(alumni.avatar_url)"
                  class="alumni-avatar"
                />
                <div class="alumni-info">
                  <h4 class="alumni-name">
                    {{ alumni.username }}
                    <el-tag v-if="alumni.gender" size="small" :type="alumni.gender === '女' ? 'danger' : ''">
                      {{ alumni.gender }}
                    </el-tag>
                  </h4>
                  <p class="alumni-major" v-if="alumni.major">{{ alumni.major }}</p>
                  <p class="alumni-year" v-if="alumni.enrollment_year">
                    <el-icon><Calendar /></el-icon>
                    {{ alumni.enrollment_year }}级
                  </p>
                  <p class="alumni-bio" v-if="alumni.bio">{{ alumni.bio }}</p>
                </div>
                <div class="alumni-actions">
                  <el-button 
                    type="primary" 
                    size="small"
                    @click.stop="sendMessage(alumni.id)"
                  >
                    私信
                  </el-button>
                </div>
              </div>
            </div>
            
            <el-empty v-else description="暂无符合条件的校友" />
            
            <!-- 分页 -->
            <div class="pagination" v-if="total > 0">
              <el-pagination
                v-model:current-page="page"
                :page-size="perPage"
                :total="total"
                layout="prev, pager, next"
                @current-change="fetchAlumni"
              />
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { School, Search, Calendar } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { alumniApi } from '@/api/alumni'

const router = useRouter()
const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const alumniList = ref([])
const yearOptions = ref([])
const page = ref(1)
const perPage = ref(20)
const total = ref(0)

const stats = ref({
  school_name: '',
  total_alumni: 0,
  same_year_count: 0,
  my_year: null
})

const searchForm = reactive({
  keyword: '',
  gender: '',
  enrollment_year: ''
})

const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE_URL}${url}`
}

const fetchStats = async () => {
  try {
    const res = await alumniApi.getAlumniStats()
    const data = res.data || res
    stats.value = data
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

const fetchYears = async () => {
  try {
    const res = await alumniApi.getAlumniYears()
    const data = res.data || res
    yearOptions.value = data.items || []
  } catch (error) {
    console.error('获取年份列表失败', error)
  }
}

const fetchAlumni = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      per_page: perPage.value,
      keyword: searchForm.keyword,
      gender: searchForm.gender,
      enrollment_year: searchForm.enrollment_year
    }
    const res = await alumniApi.getAlumniCircle(params)
    const data = res.data || res
    alumniList.value = data.items || []
    total.value = data.total || 0
    if (data.school_name && !stats.value.school_name) {
      stats.value.school_name = data.school_name
    }
  } catch (error) {
    console.error('获取校友列表失败', error)
    ElMessage.error(error.response?.data?.error || '获取校友列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchAlumni()
}

const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.gender = ''
  searchForm.enrollment_year = ''
  handleSearch()
}

const viewProfile = (userId) => {
  router.push(`/profile/${userId}`)
}

const sendMessage = (userId) => {
  router.push(`/messages/${userId}`)
}

onMounted(() => {
  fetchStats()
  fetchYears()
  fetchAlumni()
})
</script>

<style scoped>
.alumni-circle-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding-top: 60px;
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 40px 0;
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.school-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.school-text h1 {
  margin: 0 0 8px 0;
  color: #fff;
  font-size: 32px;
}

.school-text p {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}

.stats-cards {
  display: flex;
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 16px 32px;
  border-radius: 12px;
  text-align: center;
  color: #fff;
}

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: bold;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-card {
  margin-bottom: 10px;
}

.alumni-list-card {
  min-height: 500px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-text {
  color: #909399;
  font-size: 14px;
}

.alumni-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.alumni-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.alumni-item:hover {
  background: #e6f2ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.alumni-avatar {
  flex-shrink: 0;
}

.alumni-info {
  flex: 1;
  min-width: 0;
}

.alumni-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.alumni-major {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #606266;
}

.alumni-year {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.alumni-bio {
  margin: 0;
  font-size: 13px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alumni-actions {
  flex-shrink: 0;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .school-info {
    flex-direction: column;
  }
  
  .alumni-grid {
    grid-template-columns: 1fr;
  }
}
</style>
