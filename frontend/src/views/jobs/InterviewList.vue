<template>
  <div class="interview-list-page">
    <div class="page-header">
      <div class="container">
        <h1>面试经验</h1>
        <p>分享和浏览真实的面试经历，助力求职成功</p>
        <el-button 
          v-if="userStore.isLoggedIn" 
          type="primary" 
          size="large"
          @click="showPublish = true"
        >
          <el-icon><Edit /></el-icon>
          分享我的经验
        </el-button>
      </div>
    </div>

    <div class="container main-content">
      <div class="filter-bar">
        <el-input v-model="searchQuery" placeholder="搜索公司或职位" clearable>
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="filterResult" placeholder="面试结果" clearable>
          <el-option label="获得Offer" value="offer" />
          <el-option label="未通过" value="rejected" />
          <el-option label="等待结果" value="pending" />
        </el-select>
      </div>

      <div class="experience-list">
        <el-card v-for="exp in experiences" :key="exp.id" shadow="hover" @click="viewDetail(exp.id)">
          <div class="exp-header">
            <h3>{{ exp.company_name }}</h3>
            <el-tag :type="resultType(exp.result)">{{ resultText(exp.result) }}</el-tag>
          </div>
          <p class="exp-preview">{{ previewContent(exp.content) }}</p>
          <div class="exp-stats">
            <span>{{ exp.view_count }} 浏览</span>
            <span>{{ exp.helpful_count }} 赞</span>
          </div>
        </el-card>
        <el-empty v-if="experiences.length === 0" description="暂无面试经验" />
      </div>
    </div>

    <el-dialog v-model="showPublish" title="分享面试经验" width="700px">
      <el-form :model="publishForm" label-width="100px">
        <el-form-item label="公司名称" required>
          <el-input v-model="publishForm.company_name" />
        </el-form-item>
        <el-form-item label="难度">
          <el-rate v-model="publishForm.difficulty" show-score />
        </el-form-item>
        <el-form-item label="面试结果">
          <el-radio-group v-model="publishForm.result">
            <el-radio label="offer">获得Offer</el-radio>
            <el-radio label="rejected">未通过</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="经验内容" required>
          <el-input v-model="publishForm.content" type="textarea" :rows="8" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPublish = false">取消</el-button>
        <el-button type="primary" @click="submitExperience" :loading="publishing">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { Edit, Search } from '@element-plus/icons-vue'
import { getInterviewExperiences, createInterviewExperience } from '@/api/interview'

const router = useRouter()
const userStore = useUserStore()
const experiences = ref([])
const searchQuery = ref('')
const filterResult = ref('')
const showPublish = ref(false)
const publishing = ref(false)
const publishForm = ref({ company_name: '', difficulty: 3, result: 'offer', content: '' })

const fetchExperiences = async () => {
  try {
    const res = await getInterviewExperiences({ company: searchQuery.value, result: filterResult.value })
    experiences.value = res.data.items
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const viewDetail = (id) => router.push(`/interview/${id}`)

const submitExperience = async () => {
  publishing.value = true
  try {
    await createInterviewExperience(publishForm.value)
    ElMessage.success('发布成功')
    showPublish.value = false
    fetchExperiences()
  } catch (error) {
    ElMessage.error('发布失败')
  } finally {
    publishing.value = false
  }
}

const resultType = (result) => ({ offer: 'success', rejected: 'danger', pending: 'warning' }[result] || 'info')
const resultText = (result) => ({ offer: 'Offer', rejected: '未通过', pending: '等待中' }[result])
const previewContent = (content) => content?.length > 200 ? content.substring(0, 200) + '...' : content

onMounted(fetchExperiences)
</script>

<style scoped>
.interview-list-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 60px 0; text-align: center; }
.page-header h1 { font-size: 36px; margin-bottom: 16px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
.main-content { padding: 30px 0; }
.filter-bar { display: flex; gap: 16px; margin-bottom: 24px; }
.experience-list { display: flex; flex-direction: column; gap: 16px; }
.exp-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.exp-preview { color: #666; margin-bottom: 12px; }
.exp-stats { color: #999; font-size: 14px; display: flex; gap: 20px; }
</style>
