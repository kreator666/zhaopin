<template>
  <div class="my-events-page">
    <Navbar />
    
    <div class="container" style="padding-top: 80px;">
      <el-card>
        <template #header>
          <div class="card-header">
            <h2>我的活动</h2>
            <el-button type="primary" @click="goToCreate">
              <el-icon><Plus /></el-icon>
              发布活动
            </el-button>
          </div>
        </template>
        
        <!-- Tab 切换 -->
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="我参加的" name="joined">
            <div v-loading="loading" class="events-list">
              <event-list-item 
                v-for="event in events" 
                :key="event.id"
                :event="event"
                @click="goToDetail(event.id)"
              />
              <el-empty v-if="!loading && events.length === 0" description="暂无参加的活动" />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="我发起的" name="created">
            <div v-loading="loading" class="events-list">
              <event-list-item 
                v-for="event in events" 
                :key="event.id"
                :event="event"
                :is-creator="true"
                @click="goToDetail(event.id)"
              />
              <el-empty v-if="!loading && events.length === 0" description="暂无发起的活动" />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="历史活动" name="history">
            <div v-loading="loading" class="events-list">
              <event-list-item 
                v-for="event in events" 
                :key="event.id"
                :event="event"
                @click="goToDetail(event.id)"
              />
              <el-empty v-if="!loading && events.length === 0" description="暂无历史活动" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import EventListItem from './components/EventListItem.vue'
import { socialApi } from '@/api/social'

const router = useRouter()

const activeTab = ref('joined')
const loading = ref(false)
const events = ref([])

// 获取活动列表
const fetchEvents = async () => {
  loading.value = true
  try {
    const res = await socialApi.getMyEvents(activeTab.value)
    events.value = res.data.items || []
  } catch (err) {
    console.error('获取活动失败:', err)
  } finally {
    loading.value = false
  }
}

const handleTabChange = () => {
  fetchEvents()
}

const goToDetail = (id) => {
  router.push(`/social/events/${id}`)
}

const goToCreate = () => {
  router.push('/social/events/create')
}

onMounted(() => {
  fetchEvents()
})
</script>

<script>
// 局部组件
export default {
  components: {
    EventListItem
  }
}
</script>

<style scoped>
.my-events-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 900px;
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
  font-size: 20px;
}

.events-list {
  min-height: 300px;
}
</style>
