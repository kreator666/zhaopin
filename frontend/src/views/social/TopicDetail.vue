<template>
  <div class="topic-detail-page">
    <Navbar />
    
    <div class="container" style="padding-top: 80px;">
      <!-- 返回按钮 -->
      <div class="back-nav">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-wrapper">
        <el-skeleton :rows="10" animated />
      </div>
      
      <!-- 话题内容 -->
      <template v-else-if="topic">
        <el-card class="topic-card">
          <div class="topic-header">
            <div class="author-info">
              <el-avatar :size="50" :src="topic.user?.avatar_url" />
              <div class="author-meta">
                <div class="username">{{ topic.user?.username || '匿名用户' }}</div>
                <div class="post-time">{{ formatTime(topic.created_at) }}</div>
              </div>
            </div>
            <div class="topic-actions">
              <el-tag v-if="topic.is_pinned" type="danger" effect="dark">置顶</el-tag>
              <el-tag v-if="topic.status === 'solved'" type="success">已解决</el-tag>
              <el-tag v-if="topic.status === 'closed'" type="info">已关闭</el-tag>
              
              <el-dropdown v-if="isAuthor" @command="handleCommand">
                <el-button link>
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
                    <el-dropdown-item command="close" v-if="topic.status === 'open'">关闭话题</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          
          <h1 class="topic-title">{{ topic.title }}</h1>
          
          <div class="topic-content">{{ topic.content }}</div>
          
          <div class="topic-tags" v-if="topic.tags && topic.tags.length > 0">
            <el-tag 
              v-for="tag in topic.tags" 
              :key="tag" 
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </div>
          
          <div class="topic-stats">
            <span><el-icon><View /></el-icon> {{ topic.view_count || 0 }} 浏览</span>
            <span><el-icon><ChatDotRound /></el-icon> {{ topic.reply_count || 0 }} 回复</span>
          </div>
        </el-card>
        
        <!-- 回复区域 -->
        <el-card class="replies-card">
          <template #header>
            <div class="replies-header">
              <span>全部回复 ({{ replies.length }})</span>
            </div>
          </template>
          
          <!-- 回复输入框 -->
          <div v-if="topic.status === 'open'" class="reply-input-section">
            <el-input
              v-model="replyContent"
              type="textarea"
              :rows="4"
              placeholder="写下你的回复..."
              maxlength="1000"
              show-word-limit
            />
            <div class="reply-actions">
              <el-button type="primary" @click="submitReply" :loading="replyLoading">
                发表回复
              </el-button>
            </div>
          </div>
          
          <el-alert
            v-else
            :title="topic.status === 'solved' ? '话题已解决' : '话题已关闭'"
            type="info"
            :closable="false"
          />
          
          <!-- 回复列表 -->
          <div class="replies-list" v-loading="repliesLoading">
            <el-empty v-if="replies.length === 0" description="暂无回复，来说两句吧" />
            
            <div
              v-for="reply in replies"
              :key="reply.id"
              class="reply-item"
              :class="{ 'accepted': reply.is_accepted }"
            >
              <div class="reply-header">
                <div class="author-info">
                  <el-avatar :size="36" :src="reply.user?.avatar_url" />
                  <div class="author-meta">
                    <span class="username">{{ reply.user?.username || '匿名用户' }}</span>
                    <span class="time">{{ formatTime(reply.created_at) }}</span>
                  </div>
                </div>
                
                <div class="reply-actions">
                  <el-tag v-if="reply.is_accepted" type="success" effect="dark">
                    <el-icon><Check /></el-icon> 最佳答案
                  </el-tag>
                  
                  <el-button
                    v-if="isAuthor && !reply.is_accepted && topic.status === 'open'"
                    link
                    type="success"
                    @click="acceptReply(reply.id)"
                  >
                    采纳
                  </el-button>
                  
                  <el-button
                    v-if="reply.user_id === currentUserId"
                    link
                    type="danger"
                    @click="deleteReply(reply.id)"
                  >
                    删除
                  </el-button>
                </div>
              </div>
              
              <div class="reply-content">{{ reply.content }}</div>
            </div>
          </div>
        </el-card>
      </template>
      
      <!-- 错误状态 -->
      <el-result
        v-else
        icon="error"
        title="话题不存在或已被删除"
      >
        <template #extra>
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </template>
      </el-result>
    </div>
    
    <!-- 编辑话题弹窗 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑话题"
      width="600px"
    >
      <el-form :model="editForm" label-position="top">
        <el-form-item label="标题">
          <el-input v-model="editForm.title" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="editForm.content" type="textarea" :rows="6" maxlength="2000" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="submitEdit" :loading="editLoading">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, View, ChatDotRound, Check, More } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { socialApi } from '@/api/social'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const topicId = computed(() => route.params.id)
const currentUserId = computed(() => userStore.userInfo?.id)

// 话题数据
const loading = ref(true)
const topic = ref(null)
const isAuthor = computed(() => topic.value?.user_id === currentUserId.value)

// 回复数据
const replies = ref([])
const repliesLoading = ref(false)
const replyContent = ref('')
const replyLoading = ref(false)

// 编辑
const showEditDialog = ref(false)
const editLoading = ref(false)
const editForm = ref({ title: '', content: '' })

// 获取话题详情
const fetchTopic = async () => {
  loading.value = true
  try {
    const res = await socialApi.getTopic(topicId.value)
    topic.value = res.data
  } catch (err) {
    console.error('获取话题失败:', err)
    topic.value = null
  } finally {
    loading.value = false
  }
}

// 获取回复列表
const fetchReplies = async () => {
  repliesLoading.value = true
  try {
    const res = await socialApi.getTopicReplies(topicId.value)
    replies.value = res.data.items || []
  } catch (err) {
    console.error('获取回复失败:', err)
  } finally {
    repliesLoading.value = false
  }
}

// 发表回复
const submitReply = async () => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  
  replyLoading.value = true
  try {
    await socialApi.createTopicReply(topicId.value, {
      content: replyContent.value
    })
    
    ElMessage.success('回复成功')
    replyContent.value = ''
    fetchReplies()
    fetchTopic()
  } catch (err) {
    console.error('回复失败:', err)
    ElMessage.error(err.response?.data?.error || '回复失败')
  } finally {
    replyLoading.value = false
  }
}

// 采纳回复
const acceptReply = async (replyId) => {
  try {
    await ElMessageBox.confirm('确定将此回复采纳为最佳答案？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await socialApi.acceptTopicReply(replyId)
    ElMessage.success('已采纳')
    fetchReplies()
    fetchTopic()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('采纳失败:', err)
      ElMessage.error('采纳失败')
    }
  }
}

// 删除回复
const deleteReply = async (replyId) => {
  try {
    await ElMessageBox.confirm('确定删除此回复？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await socialApi.deleteTopicReply(replyId)
    ElMessage.success('删除成功')
    fetchReplies()
    fetchTopic()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'edit':
      editForm.value = {
        title: topic.value.title,
        content: topic.value.content
      }
      showEditDialog.value = true
      break
    case 'close':
      closeTopic()
      break
    case 'delete':
      deleteTopic()
      break
  }
}

// 编辑话题
const submitEdit = async () => {
  if (!editForm.value.title.trim()) {
    ElMessage.warning('请输入标题')
    return
  }
  
  editLoading.value = true
  try {
    await socialApi.updateTopic(topicId.value, editForm.value)
    ElMessage.success('更新成功')
    showEditDialog.value = false
    fetchTopic()
  } catch (err) {
    console.error('更新失败:', err)
    ElMessage.error('更新失败')
  } finally {
    editLoading.value = false
  }
}

// 关闭话题
const closeTopic = async () => {
  try {
    await ElMessageBox.confirm('确定关闭此话题？关闭后无法继续回复', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await socialApi.closeTopic(topicId.value)
    ElMessage.success('话题已关闭')
    fetchTopic()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('关闭失败:', err)
      ElMessage.error('关闭失败')
    }
  }
}

// 删除话题
const deleteTopic = async () => {
  try {
    await ElMessageBox.confirm('确定删除此话题？此操作不可恢复', '警告', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'danger'
    })
    
    await socialApi.deleteTopic(topicId.value)
    ElMessage.success('删除成功')
    goBack()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 返回列表
const goBack = () => {
  router.push('/social/circles')
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchTopic()
  fetchReplies()
})
</script>

<style scoped>
.topic-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-nav {
  margin-bottom: 20px;
}

.loading-wrapper {
  padding: 40px;
  background: white;
  border-radius: 8px;
}

.topic-card {
  margin-bottom: 20px;
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.author-info {
  display: flex;
  gap: 12px;
}

.author-meta {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 500;
  font-size: 16px;
  color: #333;
}

.post-time {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

.topic-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.topic-title {
  margin: 0 0 16px 0;
  font-size: 24px;
  color: #333;
  line-height: 1.4;
}

.topic-content {
  font-size: 15px;
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap;
  margin-bottom: 20px;
}

.topic-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.tag-item {
  margin-right: 0;
}

.topic-stats {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 14px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.topic-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.replies-card {
  margin-bottom: 40px;
}

.replies-header {
  font-weight: 500;
  font-size: 16px;
}

.reply-input-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.reply-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.replies-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.reply-item {
  padding: 16px;
  border-radius: 8px;
  background: #f9f9f9;
}

.reply-item.accepted {
  background: #f0f9f0;
  border: 1px solid #67c23a;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.reply-header .author-info {
  align-items: center;
}

.reply-header .username {
  font-size: 14px;
}

.reply-header .time {
  font-size: 12px;
  color: #999;
}

.reply-content {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}
</style>
