<template>
  <div class="event-list-page">
    <Navbar />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <h1>活动约伴</h1>
        <p>学习、运动、娱乐，一起约起来</p>
        <el-button type="primary" size="large" @click="goToCreate" v-if="userStore.isLoggedIn">
          <el-icon><Plus /></el-icon>
          发布活动
        </el-button>
      </div>
    </div>
    
    <div class="container main-content">
      <!-- 筛选栏 -->
      <el-card class="filter-card" shadow="never">
        <div class="filter-row">
          <div class="filter-left">
            <!-- 活动类型 -->
            <el-radio-group v-model="filter.type" @change="handleFilterChange">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button 
                v-for="t in eventTypes" 
                :key="t.value" 
                :label="t.value"
              >
                {{ t.label }}
              </el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="filter-right">
            <!-- 时间筛选 -->
            <el-date-picker
              v-model="filter.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              @change="handleFilterChange"
              style="width: 240px"
            />
            
            <!-- 搜索 -->
            <el-input
              v-model="filter.keyword"
              placeholder="搜索活动"
              clearable
              @keyup.enter="handleFilterChange"
              style="width: 200px"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </el-card>
      
      <!-- 骨架屏 -->
      <div v-if="loading" class="event-grid">
        <div v-for="i in 6" :key="i" class="event-card skeleton">
          <el-skeleton animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 100%; height: 160px" />
              <div style="padding: 16px">
                <el-skeleton-item variant="h3" style="width: 80%; margin-bottom: 12px" />
                <el-skeleton-item variant="text" style="width: 60%; margin-bottom: 8px" />
                <el-skeleton-item variant="text" style="width: 40%" />
              </div>
            </template>
          </el-skeleton>
        </div>
      </div>
      
      <!-- 活动列表 -->
      <div v-else class="events-list">
        <el-empty 
          v-if="events.length === 0" 
          description="暂无活动，来发布第一个吧！"
        />
        
        <div v-else class="event-grid">
          <div
            v-for="event in events"
            :key="event.id"
            class="event-card"
            @click="goToDetail(event.id)"
          >
            <!-- 封面图 -->
            <div class="event-cover">
              <el-image 
                :src="event.cover_image || defaultCover" 
                fit="cover"
                class="cover-img"
              >
                <template #error>
                  <div class="cover-placeholder">
                    <el-icon :size="40"><Calendar /></el-icon>
                  </div>
                </template>
              </el-image>
              
              <!-- 状态标签 -->
              <div class="event-status" :class="event.status">
                {{ statusText(event.status) }}
              </div>
              
              <!-- 费用标签 -->
              <div class="event-fee" v-if="event.fee_type !== 'free'">
                {{ feeText(event.fee_type, event.fee_amount) }}
              </div>
            </div>
            
            <!-- 内容区 -->
            <div class="event-content">
              <h3 class="event-title">{{ event.title }}</h3>
              
              <div class="event-meta">
                <span class="meta-item">
                  <el-icon><Calendar /></el-icon>
                  {{ formatDate(event.start_time) }}
                </span>
                <span class="meta-item">
                  <el-icon><Location /></el-icon>
                  {{ event.location }}
                </span>
              </div>
              
              <div class="event-type">
                <el-tag size="small" effect="plain">
                  {{ getTypeLabel(event.event_type) }}
                </el-tag>
              </div>
              
              <div class="event-footer">
                <div class="participant-info">
                  <el-avatar-group :size="24" :max="3">
                    <el-avatar 
                      v-for="p in event.participants?.slice(0, 3)" 
                      :key="p.id"
                      :src="p.avatar_url"
                    />
                  </el-avatar-group>
                  <span class="participant-count">
                    {{ event.current_participants || 0 }}
                    <template v-if="event.max_participants">
                      / {{ event.max_participants }}
                    </template>
                    人
                  </span>
                </div>
                
                <el-button 
                  :type="joinButtonType(event)"
                  :disabled="!canJoin(event)"
                  size="small"
                  @click.stop="handleJoin(event)"
                  :loading="joinLoading === event.id"
                >
                  {{ joinButtonText(event) }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @change="fetchEvents"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Search, Calendar, Location } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { socialApi } from '@/api/social'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 默认封面
const defaultCover = 'https://placehold.co/400x200/667eea/ffffff?text=Activity'

// 数据
const loading = ref(false)
const events = ref([])
const eventTypes = ref([])
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)
const joinLoading = ref(null)

// 筛选条件
const filter = reactive({
  type: '',
  keyword: '',
  dateRange: null
})

// 状态映射
const statusMap = {
  open: '报名中',
  full: '已满员',
  ongoing: '进行中',
  ended: '已结束',
  cancelled: '已取消'
}

const statusText = (status) => statusMap[status] || status

// 费用文本
const feeText = (type, amount) => {
  if (type === 'free') return '免费'
  if (type === 'aa') return 'AA制'
  if (type === 'fixed') return `¥${amount / 100}`
  return ''
}

// 获取类型标签
const getTypeLabel = (value) => {
  const type = eventTypes.value.find(t => t.value === value)
  return type?.label || value
}

// 获取活动列表
const fetchEvents = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      per_page: pageSize.value,
      type: filter.type,
      keyword: filter.keyword || undefined,
      start_date: filter.dateRange?.[0],
      end_date: filter.dateRange?.[1]
    }
    
    const res = await socialApi.getEvents(params)
    events.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (err) {
    console.error('获取活动列表失败:', err)
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

// 获取活动类型
const fetchEventTypes = async () => {
  try {
    const res = await socialApi.getEventTypes()
    eventTypes.value = res.data.items || []
  } catch (err) {
    console.error('获取活动类型失败:', err)
  }
}

// 筛选变化
const handleFilterChange = () => {
  page.value = 1
  fetchEvents()
}

// 是否可以报名
const canJoin = (event) => {
  if (!userStore.isLoggedIn) return false
  if (event.creator_id === userStore.userInfo?.id) return false
  return ['open', 'full'].includes(event.status)
}

// 报名按钮类型
const joinButtonType = (event) => {
  if (event.status === 'full') return 'info'
  if (event.status === 'ended') return 'info'
  return 'primary'
}

// 报名按钮文本
const joinButtonText = (event) => {
  if (event.status === 'full') return '已满员'
  if (event.status === 'ended') return '已结束'
  if (event.status === 'ongoing') return '进行中'
  if (event.creator_id === userStore.userInfo?.id) return '我发布的'
  return '我要报名'
}

// 处理报名
const handleJoin = async (event) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  joinLoading.value = event.id
  try {
    await socialApi.joinEvent(event.id)
    ElMessage.success('报名成功')
    fetchEvents()
  } catch (err) {
    console.error('报名失败:', err)
    ElMessage.error(err.response?.data?.error || '报名失败')
  } finally {
    joinLoading.value = null
  }
}

// 跳转到详情
const goToDetail = (id) => {
  router.push(`/social/events/${id}`)
}

// 跳转到创建
const goToCreate = () => {
  router.push('/social/events/create')
}

// 格式化日期
const formatDate = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
  fetchEventTypes()
  fetchEvents()
})
</script>

<style scoped>
.event-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #67C23A 0%, #E6A23C 100%);
  color: white;
  padding: 50px 0;
  text-align: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 36px;
}

.page-header p {
  margin: 0 0 20px 0;
  font-size: 16px;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.main-content {
  padding: 20px 0 40px;
}

/* 筛选栏 */
.filter-card {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-right {
  display: flex;
  gap: 12px;
}

/* 活动列表 */
.events-list {
  min-height: 400px;
}

.event-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.event-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.event-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.event-card.skeleton {
  cursor: default;
}

.event-card.skeleton:hover {
  transform: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* 封面 */
.event-cover {
  position: relative;
  height: 160px;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.event-status {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.event-status.open {
  background: #67c23a;
  color: white;
}

.event-status.full {
  background: #f56c6c;
  color: white;
}

.event-status.ongoing {
  background: #e6a23c;
  color: white;
}

.event-status.ended,
.event-status.cancelled {
  background: #909399;
  color: white;
}

.event-fee {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  background: rgba(0,0,0,0.6);
  color: white;
  border-radius: 4px;
  font-size: 12px;
}

/* 内容区 */
.event-content {
  padding: 16px;
}

.event-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
}

.event-type {
  margin-bottom: 12px;
}

.event-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.participant-count {
  font-size: 13px;
  color: #666;
}

/* 分页 */
.pagination-wrapper {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 响应式 */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-right {
    width: 100%;
    flex-direction: column;
  }
  
  .filter-right :deep(.el-date-editor) {
    width: 100% !important;
  }
  
  .filter-right .el-input {
    width: 100% !important;
  }
  
  .event-grid {
    grid-template-columns: 1fr;
  }
}
</style>
