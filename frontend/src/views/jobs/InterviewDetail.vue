<template>
  <div class="interview-detail-page" v-if="experience.id">
    <div class="container">
      <el-card shadow="never">
        <div class="header">
          <h1>{{ experience.company_name }}</h1>
          <el-tag :type="resultType(experience.result)" size="large">{{ resultText(experience.result) }}</el-tag>
        </div>
        <div class="meta">
          难度：<el-rate :model-value="experience.difficulty" disabled />
          <span>{{ formatTime(experience.created_at) }}</span>
        </div>
        <div class="content" v-html="formattedContent"></div>
        <div class="actions">
          <el-button type="primary" :icon="Star" @click="markHelpful">有帮助 ({{ experience.helpful_count }})</el-button>
          <el-button :icon="Share" @click="shareExperience">分享</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, Share } from '@element-plus/icons-vue'
import { getInterviewExperience, markHelpful as markHelpfulApi } from '@/api/interview'

const route = useRoute()
const experience = ref({})
const formattedContent = computed(() => experience.value.content?.replace(/\n/g, '<br>') || '')

const fetchExperience = async () => {
  try {
    const res = await getInterviewExperience(route.params.id)
    experience.value = res.data
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

const markHelpful = async () => {
  try {
    await markHelpfulApi(experience.value.id)
    experience.value.helpful_count++
    ElMessage.success('已标记为有帮助')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const shareExperience = () => {
  navigator.clipboard.writeText(window.location.href)
  ElMessage.success('链接已复制')
}

const resultType = (result) => ({ offer: 'success', rejected: 'danger', pending: 'warning' }[result] || 'info')
const resultText = (result) => ({ offer: '获得Offer', rejected: '未通过', pending: '等待结果' }[result])
const formatTime = (time) => time ? new Date(time).toLocaleString('zh-CN') : ''

onMounted(fetchExperience)
</script>

<style scoped>
.interview-detail-page { min-height: 100vh; background: #f5f7fa; padding: 30px 0; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.header h1 { margin: 0; }
.meta { color: #666; margin-bottom: 20px; display: flex; gap: 20px; align-items: center; }
.content { font-size: 16px; line-height: 1.8; margin-bottom: 20px; }
.actions { display: flex; gap: 16px; }
</style>
