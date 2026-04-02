<template>
  <div class="campus-talks-page">
    <div class="page-header">
      <div class="container">
        <h1>校园宣讲会</h1>
        <p>最新校园招聘信息，不错过每一个机会</p>
      </div>
    </div>

    <div class="container main-content">
      <div class="filter-bar">
        <el-input v-model="searchSchool" placeholder="搜索学校" clearable />
        <el-select v-model="filterStatus" placeholder="状态" clearable>
          <el-option label="即将开始" value="upcoming" />
          <el-option label="已结束" value="ended" />
        </el-select>
      </div>

      <div class="talks-list">
        <el-card v-for="talk in talks" :key="talk.id" shadow="hover">
          <div class="talk-header">
            <h3>{{ talk.title }}</h3>
            <el-tag :type="statusType(talk.status)">{{ statusText(talk.status) }}</el-tag>
          </div>
          <p><el-icon><School /></el-icon> {{ talk.school_name }}</p>
          <p><el-icon><Calendar /></el-icon> {{ formatDateTime(talk.start_time) }}</p>
          <p class="description">{{ talk.description }}</p>
          <el-button v-if="talk.registration_url && talk.status !== 'ended'" type="success" @click="openRegistration(talk.registration_url)">立即报名</el-button>
        </el-card>
        <el-empty v-if="talks.length === 0" description="暂无宣讲会" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { School, Calendar } from '@element-plus/icons-vue'
import { getCampusTalks } from '@/api/interview'

const talks = ref([])
const searchSchool = ref('')
const filterStatus = ref('')

const fetchTalks = async () => {
  try {
    const res = await getCampusTalks({ school: searchSchool.value, status: filterStatus.value })
    talks.value = res.data.items
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const openRegistration = (url) => window.open(url, '_blank')
const statusType = (status) => ({ upcoming: 'primary', ongoing: 'success', ended: 'info' }[status] || 'info')
const statusText = (status) => ({ upcoming: '即将开始', ongoing: '进行中', ended: '已结束' }[status])
const formatDateTime = (datetime) => datetime ? new Date(datetime).toLocaleString('zh-CN') : ''

onMounted(fetchTalks)
</script>

<style scoped>
.campus-talks-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: #fff; padding: 60px 0; text-align: center; }
.page-header h1 { font-size: 36px; margin-bottom: 16px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
.main-content { padding: 30px 0; }
.filter-bar { display: flex; gap: 16px; margin-bottom: 24px; }
.talks-list { display: flex; flex-direction: column; gap: 20px; }
.talk-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.talk-header h3 { margin: 0; }
.description { color: #666; margin: 12px 0; }
</style>
